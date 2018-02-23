var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // BASE_API: '"http://192.168.174.144:2222"', // api的base_url
  // BASE_API: '"http://119.29.186.141:8080"' // api的base_url
  BASE_API: '"http://localhost:8080"'//
})
