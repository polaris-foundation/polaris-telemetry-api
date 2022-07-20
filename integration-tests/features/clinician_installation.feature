Feature: Manage clinicians installations
  As a support person
  I want to have up to date information about clinicians' installations
  So that I can better troubleshoot any issues
  
  Scenario: Clinician's installation is created and retrieved by uuid
    Given there exists a clinician
    When clinician's installation is stored
    Then the installation details are returned
    When the clinician's installation is retrieved by its uuid
    Then the installation details are returned

  Scenario: Latest installation for clinician with multiple installations
    Given there exists a clinician
    And clinician's installation is stored
    And clinician's latest installation is retrieved
    And the latest installation details are returned
    When another clinician's installation is stored
    And clinician's latest installation is retrieved
    Then the latest installation details are returned

  Scenario: Clinician's installation is updated
    Given there exists a clinician
    And clinician's installation is stored
    When the clinician's installation is updated
    And the clinician's installation is retrieved by its uuid
    Then the installation details are returned

  Scenario: Another clinician's installation is created with greater application version
    Given there exists a clinician
    And clinician's installation is stored
    When another clinician's installation, but with greater application version is stored
    And clinician's latest installation is retrieved
    Then the latest installation details are returned
