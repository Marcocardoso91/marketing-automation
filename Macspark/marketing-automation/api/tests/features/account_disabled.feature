Feature: Account Disabled Alert
  Scenario: Detect disabled account and send critical alert
    Given the Facebook account is inactive for more than 15 minutes
    When the collector identifies status "disabled"
    Then a CRITICAL alert should be sent via Slack and WhatsApp
    And the event must be stored with timestamp and delivery confirmation
