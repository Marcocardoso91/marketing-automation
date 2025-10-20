/**
 * Authentication API Endpoints
 * Dashboard Sabrina Costa
 */

const express = require('express');
const bcrypt = require('bcryptjs');
const { query } = require('../db/connection');
const { sign, authenticateJWT } = require('../utils/jwt');

const router = express.Router();

/**
 * POST /api/auth/login
 * Authenticate user and return JWT token
 */
router.post('/login', async (req, res, next) => {
    try {
        const { email, password } = req.body;
        
        // Validate input
        if (!email || !password) {
            return res.status(400).json({
                success: false,
                error: 'Email e senha são obrigatórios'
            });
        }
        
        // Find user by email
        const result = await query(
            'SELECT id, email, password_hash, name, role FROM users WHERE email = $1',
            [email]
        );
        
        if (result.rows.length === 0) {
            return res.status(401).json({
                success: false,
                error: 'Credenciais inválidas'
            });
        }
        
        const user = result.rows[0];
        
        // Verify password
        const passwordMatch = await bcrypt.compare(password, user.password_hash);
        
        if (!passwordMatch) {
            return res.status(401).json({
                success: false,
                error: 'Credenciais inválidas'
            });
        }
        
        // Generate JWT token
        const token = sign({
            userId: user.id,
            email: user.email,
            role: user.role
        });
        
        // Return success
        res.json({
            success: true,
            token,
            expiresIn: process.env.JWT_EXPIRES_IN || '7d',
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role
            }
        });
        
    } catch (error) {
        next(error);
    }
});

/**
 * POST /api/auth/logout
 * Logout user (client-side token removal is sufficient)
 */
router.post('/logout', authenticateJWT, async (req, res) => {
    // In a more complex setup, you might blacklist the token here
    res.json({
        success: true,
        message: 'Logout realizado com sucesso'
    });
});

/**
 * GET /api/auth/me
 * Get current authenticated user info
 */
router.get('/me', authenticateJWT, async (req, res, next) => {
    try {
        const result = await query(
            'SELECT id, email, name, role, created_at FROM users WHERE id = $1',
            [req.user.userId]
        );
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                error: 'Usuário não encontrado'
            });
        }
        
        res.json({
            success: true,
            user: result.rows[0]
        });
        
    } catch (error) {
        next(error);
    }
});

module.exports = router;

