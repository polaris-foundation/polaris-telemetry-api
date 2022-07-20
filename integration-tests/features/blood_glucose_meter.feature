Feature: Manage patients installations
  As a QARA representative
  I want to know that the blood glucose readings are accurate
  So that I can be confident that the application is working as expected
  
  Scenario: Blood glucose meter is created and retrieved by uuid
    Given there exists a patient
    When the meter is stored
    Then the blood glucose meter is returned
    When the blood glucose meter is requested by its uuid
    Then the blood glucose meter is returned
