module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': 'google',
  'overrides': [
  ],
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module',
  },
  'rules': {
    'camelcase': 'off',
    'max-len': 'off',
    'require-jsdoc': 'off',
    'new-cap': 'off',
  },
  'parser': '@babel/eslint-parser',
  'parserOptions': {
    'requireConfigFile': false,
  },
};
