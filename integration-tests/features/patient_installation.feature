Feature: Manage patients installations
  As a support person
  I want to have up to date information about patients' installations
  So that I can better troubleshoot any issues
  
  Scenario: Patient's installation is created and retrieved by uuid
    Given there exists a patient
    When patient's installation is stored
    Then the installation details are returned
    When the patient's installation is retrieved by its uuid
    Then the installation details are returned

  Scenario: Latest installation for patient with multiple installations
    Given there exists a patient
    And patient's installation is stored
    And patient's latest installation is retrieved
    And the latest installation details are returned
    When another patient's installation is stored
    And patient's latest installation is retrieved
    Then the latest installation details are returned

  Scenario: Patient's installation is updated
    Given there exists a patient
    And patient's installation is stored
    When the patient's installation is updated
    And the patient's installation is retrieved by its uuid
    Then the installation details are returned
