module.exports = {
    apps: [{
        name: 'font.jarosh.info',
        script: 'app.js',
        env: {
            NODE_ENV: 'production'
        },
        env_dev: {
            NODE_ENV: 'development'
        }
    }]
};
