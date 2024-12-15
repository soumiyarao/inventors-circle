/*const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  jwtSecret: process.env.JWT_SECRET || "YOUR_secret_key",
  mongoUri: process.env.MONGODB_URI ||
    process.env.MONGO_HOST ||
    'mongodb://' + (process.env.IP || 'localhost') + ':' +
    (process.env.MONGO_PORT || '27017') +
    '/inventors_circle'
}*/


const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  jwtSecret: process.env.JWT_SECRET || "YOUR_secret_key",
  mongoUri: process.env.MONGODB_URI ||
    'mongodb+srv://' + encodeURIComponent(process.env.MONGO_USER || 'Your_Username') + 
    ':' + encodeURIComponent(process.env.MONGO_PASSWORD || 'Your_Password') +
    '@' + (process.env.MONGO_CLUSTER || 'Your_cluster') +
    '/inventors_circle'
};


export default config