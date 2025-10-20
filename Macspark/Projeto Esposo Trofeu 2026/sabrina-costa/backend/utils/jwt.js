/**
 * JWT Utilities
 * Dashboard Sabrina Costa
 */

const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'default_secret_change_in_production';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';

/**
 * Generate JWT token
 */
function sign(payload) {
    return jwt.sign(payload, JWT_SECRET, {
        expiresIn: JWT_EXPIRES_IN
    });
}

/**
 * Verify JWT token
 */
function verify(token) {
    try {
        return jwt.verify(token, JWT_SECRET);
    } catch (error) {
        throw new Error('Token inválido ou expirado');
    }
}

/**
 * Decode JWT without verification (for debugging)
 */
function decode(token) {
    return jwt.decode(token);
}

/**
 * Middleware to authenticate requests
 */
function authenticateJWT(req, res, next) {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
        return res.status(401).json({
            success: false,
            error: 'Token de autenticação não fornecido'
        });
    }
    
    const token = authHeader.split(' ')[1]; // Bearer <token>
    
    try {
        const decoded = verify(token);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(403).json({
            success: false,
            error: error.message
        });
    }
}

/**
 * Middleware to check if user is admin
 */
function requireAdmin(req, res, next) {
    if (req.user.role !== 'admin') {
        return res.status(403).json({
            success: false,
            error: 'Acesso negado. Apenas administradores.'
        });
    }
    next();
}

module.exports = {
    sign,
    verify,
    decode,
    authenticateJWT,
    requireAdmin
};

