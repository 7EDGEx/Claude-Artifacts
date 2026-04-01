// Demo file for secret-scanner agent demonstration
// WARNING: This file contains intentionally fake hardcoded secrets for demo purposes only

const config = {
  // Fake AWS credentials
  aws_access_key_id: "AKIA_DUMMY_AWS_ACCESS_KEY",
  aws_secret_access_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCY_DUMMY_KEY",

  // Fake Stripe API key
  stripe_secret_key: "sk_test_DUMMY_sk_live_51ABCDEFGhijklmnopQRSTUVwxyz1234567890abcd",

  // Fake GitHub token
  github_token: "ghp_DUMMY_aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789",

  // Fake database connection string
  database_url:
    "postgres://admin:REDACTED-PASSWORD@prod-db.example.com:5432/myapp",

  // Fake JWT secret
  jwt_secret: "my_super_secret_jwt_key_do_not_share_ever",

  // Fake SendGrid API key
  sendgrid_api_key:
    "SG.DUMMY_aBcDeFgHiJkLmNoPqRsTuV.WxYz1234567890ABCDEFGhijklmnopQRSTUV",

  // Fake password
  admin_password: "P@ssw0rd!SuperSecret2024",
};

module.exports = config;
