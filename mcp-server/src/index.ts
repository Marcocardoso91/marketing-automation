#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { glob } from 'fast-glob';
import { readFileSync, statSync } from 'fs';
import { join, relative, resolve } from 'path';
import { parse } from 'gray-matter';
import { marked } from 'marked';
import Fuse from 'fuse.js';

interface DocumentMetadata {
  title: string;
  description: string;
  category: string;
  tags: string[];
  lastModified: string;
  size: number;
  path: string;
}

interface SearchResult {
  item: DocumentMetadata;
  score: number;
}

class MarketingAutomationMCPServer {
  private server: Server;
  private documents: DocumentMetadata[] = [];
  private fuse: Fuse<DocumentMetadata> | null = null;
  private projectRoot: string;

  constructor() {
    this.projectRoot = process.cwd();
    this.server = new Server(
      {
        name: 'marketing-automation-docs',
        version: '1.0.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupHandlers();
    this.loadDocuments();
  }

  private setupHandlers() {
    // List all available documentation resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: this.documents.map(doc => ({
          uri: `docs://marketing-automation/${doc.path}`,
          name: doc.title,
          description: doc.description,
          mimeType: 'text/markdown',
        })),
      };
    });

    // Read specific documentation resource
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      const path = this.extractPathFromUri(uri);
      
      if (!path) {
        throw new Error(`Invalid URI: ${uri}`);
      }

      const fullPath = join(this.projectRoot, path);
      const content = readFileSync(fullPath, 'utf-8');
      const { data: frontmatter, content: body } = parse(content);
      
      return {
        contents: [
          {
            uri,
            mimeType: 'text/markdown',
            text: body,
          },
        ],
      };
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'search_docs',
            description: 'Search documentation by query',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query',
                },
                limit: {
                  type: 'number',
                  description: 'Maximum number of results',
                  default: 10,
                },
              },
              required: ['query'],
            },
          },
          {
            name: 'get_examples',
            description: 'Get code examples for a specific feature',
            inputSchema: {
              type: 'object',
              properties: {
                feature: {
                  type: 'string',
                  description: 'Feature name to get examples for',
                },
              },
              required: ['feature'],
            },
          },
          {
            name: 'troubleshoot',
            description: 'Get troubleshooting help for an error',
            inputSchema: {
              type: 'object',
              properties: {
                error: {
                  type: 'string',
                  description: 'Error message or description',
                },
              },
              required: ['error'],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'search_docs':
          return this.searchDocs(args.query, args.limit || 10);
        
        case 'get_examples':
          return this.getExamples(args.feature);
        
        case 'troubleshoot':
          return this.troubleshoot(args.error);
        
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  private async loadDocuments() {
    const patterns = [
      'docs/**/*.md',
      'backend/docs/**/*.md',
      'analytics/docs/**/*.md',
      '*.md',
    ];

    const files = await glob(patterns, { cwd: this.projectRoot });
    
    this.documents = files.map(file => {
      const fullPath = join(this.projectRoot, file);
      const stats = statSync(fullPath);
      const content = readFileSync(fullPath, 'utf-8');
      const { data: frontmatter } = parse(content);
      
      return {
        title: frontmatter.title || this.extractTitleFromContent(content) || file,
        description: frontmatter.description || this.extractDescriptionFromContent(content),
        category: this.categorizeDocument(file),
        tags: frontmatter.tags || this.extractTagsFromContent(content),
        lastModified: stats.mtime.toISOString(),
        size: stats.size,
        path: file,
      };
    });

    // Initialize Fuse.js for fuzzy search
    this.fuse = new Fuse(this.documents, {
      keys: ['title', 'description', 'content', 'tags'],
      threshold: 0.3,
      includeScore: true,
    });
  }

  private extractPathFromUri(uri: string): string | null {
    if (!uri.startsWith('docs://marketing-automation/')) {
      return null;
    }
    return uri.replace('docs://marketing-automation/', '');
  }

  private extractTitleFromContent(content: string): string | null {
    const lines = content.split('\n');
    for (const line of lines) {
      if (line.startsWith('# ')) {
        return line.replace('# ', '').trim();
      }
    }
    return null;
  }

  private extractDescriptionFromContent(content: string): string {
    const lines = content.split('\n');
    for (const line of lines) {
      if (line.trim() && !line.startsWith('#')) {
        return line.trim().substring(0, 200);
      }
    }
    return '';
  }

  private categorizeDocument(path: string): string {
    if (path.includes('/getting-started/')) return 'getting-started';
    if (path.includes('/architecture/')) return 'architecture';
    if (path.includes('/guides/')) return 'guides';
    if (path.includes('/api/')) return 'api';
    if (path.includes('/reference/')) return 'reference';
    if (path.includes('/archive/')) return 'archive';
    return 'general';
  }

  private extractTagsFromContent(content: string): string[] {
    const tags: string[] = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
      if (line.includes('**Status:**')) tags.push('status');
      if (line.includes('**Versão:**')) tags.push('version');
      if (line.includes('**Data:**')) tags.push('dated');
      if (line.includes('TODO') || line.includes('FIXME')) tags.push('todo');
      if (line.includes('```')) tags.push('code');
      if (line.includes('http')) tags.push('links');
    }
    
    return tags;
  }

  private async searchDocs(query: string, limit: number) {
    if (!this.fuse) {
      throw new Error('Search index not initialized');
    }

    const results = this.fuse.search(query).slice(0, limit);
    
    return {
      content: [
        {
          type: 'text',
          text: `Found ${results.length} documents matching "${query}":\n\n` +
            results.map((result: SearchResult) => 
              `- **${result.item.title}** (${result.item.category})\n  ${result.item.description}\n  Score: ${result.score.toFixed(2)}`
            ).join('\n\n')
        }
      ]
    };
  }

  private async getExamples(feature: string) {
    const examples = this.documents.filter(doc => 
      doc.content?.includes(feature) || 
      doc.tags.includes(feature.toLowerCase())
    );

    if (examples.length === 0) {
      return {
        content: [
          {
            type: 'text',
            text: `No examples found for feature: ${feature}`
          }
        ]
      };
    }

    return {
      content: [
        {
          type: 'text',
          text: `Examples for ${feature}:\n\n` +
            examples.map(doc => 
              `- **${doc.title}**\n  ${doc.description}\n  Path: ${doc.path}`
            ).join('\n\n')
        }
      ]
    };
  }

  private async troubleshoot(error: string) {
    const troubleshootingDocs = this.documents.filter(doc => 
      doc.category === 'reference' && 
      doc.path.includes('troubleshooting')
    );

    const errorKeywords = error.toLowerCase().split(' ');
    const relevantDocs = troubleshootingDocs.filter(doc => 
      errorKeywords.some(keyword => 
        doc.content?.toLowerCase().includes(keyword)
      )
    );

    if (relevantDocs.length === 0) {
      return {
        content: [
          {
            type: 'text',
            text: `No specific troubleshooting found for: ${error}\n\nTry checking the general troubleshooting guide.`
          }
        ]
      };
    }

    return {
      content: [
        {
          type: 'text',
          text: `Troubleshooting help for: ${error}\n\n` +
            relevantDocs.map(doc => 
              `- **${doc.title}**\n  ${doc.description}\n  Path: ${doc.path}`
            ).join('\n\n')
        }
      ]
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Marketing Automation MCP Server running on stdio');
  }
}

// Start the server
const server = new MarketingAutomationMCPServer();
server.run().catch(console.error);
