USE BUDT702_Project_0502_04;
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'YARA')
    EXEC('CREATE SCHEMA YARA');
GO


-- 2️ DROP TABLES

DROP TABLE IF EXISTS [YARA].[Arrest];
DROP TABLE IF EXISTS [YARA].[Assign];
DROP TABLE IF EXISTS [YARA].[Contain];
DROP TABLE IF EXISTS [YARA].[Evidence];
DROP TABLE IF EXISTS [YARA].[Person];
DROP TABLE IF EXISTS [YARA].[Officer];
DROP TABLE IF EXISTS [YARA].[Incident];
GO

-- 3️ CREATE TABLES

-- INCIDENT TABLE
CREATE TABLE [YARA].[Incident] (
    incidentId CHAR(10) NOT NULL,
    incidentType VARCHAR(20),
    incidentStreet VARCHAR(20),
    incidentCity VARCHAR(20),
    incidentZip VARCHAR(10),
    incidentStatus VARCHAR(20),
    incidentDate DATETIME,
    CONSTRAINT pk_Incident_incidentId PRIMARY KEY (incidentId)
)

-- OFFICER TABLE
CREATE TABLE [YARA].[Officer] (
    officerId CHAR(10) NOT NULL,
    officerName VARCHAR(20),
    officerPhoneNumber CHAR(10),
    officerDOB DATETIME,
    officerHireDate DATETIME,
    CONSTRAINT pk_Officer_officerId PRIMARY KEY (officerId)
)

-- PERSON TABLE
CREATE TABLE [YARA].[Person] (
    personSSN CHAR(9) NOT NULL,
    personName VARCHAR(20),
    personDOB DATE,
    personPhoneNumber CHAR(10),
    CONSTRAINT pk_Person_personSSN PRIMARY KEY (personSSN)
)
-- EVIDENCE TABLE
CREATE TABLE [YARA].[Evidence] (
    evidenceId CHAR(10) NOT NULL,
    evidenceDescription VARCHAR(50),
    evidenceStorageLocation CHAR(20),
    evidenceStatus VARCHAR(20),
    incidentId CHAR(10) NOT NULL,
    CONSTRAINT pk_Evidence_evidenceId PRIMARY KEY (evidenceId),
    CONSTRAINT fk_Evidence_incidentId FOREIGN KEY (incidentId)
        REFERENCES [YARA].[Incident](incidentId)
        ON DELETE CASCADE ON UPDATE CASCADE
)

-- ASSIGN TABLE
CREATE TABLE [YARA].[Assign] (
    officerId CHAR(10) NOT NULL,
    incidentId CHAR(10) NOT NULL,
    hoursSpent INT,
    CONSTRAINT pk_Assign_officerId_incidentId PRIMARY KEY (officerId, incidentId),
    CONSTRAINT fk_Assign_officerId FOREIGN KEY (officerId)
        REFERENCES [YARA].[Officer](officerId)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    CONSTRAINT fk_Assign_incidentId FOREIGN KEY (incidentId)
        REFERENCES [YARA].[Incident](incidentId)
        ON DELETE CASCADE ON UPDATE CASCADE
)

-- CONTAIN TABLE
CREATE TABLE [YARA].[Contain] (
    incidentId CHAR(10) NOT NULL,
    personSSN CHAR(9) NOT NULL,
    role VARCHAR(10),
    CONSTRAINT pk_Contain_incidentId_personSSN PRIMARY KEY (incidentId, personSSN),
    CONSTRAINT fk_Contain_incidentId FOREIGN KEY (incidentId)
        REFERENCES [YARA].[Incident](incidentId)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Contain_personSSN FOREIGN KEY (personSSN)
        REFERENCES [YARA].[Person](personSSN)
        ON DELETE CASCADE ON UPDATE CASCADE
)

-- ARREST TABLE
CREATE TABLE [YARA].[Arrest] (
    arrestId CHAR(10) NOT NULL,
    arrestDate DATETIME,
    arrestLocation VARCHAR(20),
    arrestStatus VARCHAR(20),
    personSSN CHAR(9) NOT NULL,
    CONSTRAINT pk_Arrest_arrestId_personSSN PRIMARY KEY (arrestId, personSSN),
    CONSTRAINT fk_Arrest_personSSN FOREIGN KEY (personSSN)
        REFERENCES [YARA].[Person](personSSN)
        ON DELETE CASCADE ON UPDATE CASCADE
)


-- Select statemnets
SELECT * FROM [YARA].[Incident];
SELECT * FROM [YARA].[Officer];
SELECT * FROM [YARA].[Assign];
SELECT * FROM [YARA].[Person];
SELECT * FROM [YARA].[Evidence];
SELECT * FROM [YARA].[Arrest];
SELECT * FROM [YARA].[Contain];
GO

-- 1) List all incidents with assigned officers
SELECT 
    i.incidentId,
    i.incidentType,
    i.incidentStreet,
    i.incidentCity,
    i.incidentStatus,
    COALESCE(o.officerId, 'N/A') AS [Officer ID],
    COALESCE(o.officerName, 'N/A') AS [Officer Name],
    COALESCE(CAST(a.hoursSpent AS CHAR(10)), '0') AS [Hours Spent]
FROM [YARA].[Incident] AS i
LEFT JOIN [YARA].[Assign] AS a ON i.incidentId = a.incidentId
LEFT JOIN [YARA].[Officer] AS o ON a.officerId = o.officerId
ORDER BY i.incidentId;
GO

-- 2) Top 3 most common incident types
SELECT TOP 3
    incidentType,
    COUNT(*) AS NumberOfIncidents
FROM [YARA].[Incident]
GROUP BY incidentType
ORDER BY COUNT(*) DESC;
GO

-- 3) Officer with the most incidents handled
SELECT TOP 1
    o.officerId,
    o.officerName,
    YEAR(i.incidentDate) AS [Year],
    COUNT(DISTINCT i.incidentId) AS [TotalIncidents]
FROM [YARA].[Officer] AS o
JOIN [YARA].[Assign] AS a ON o.officerId = a.officerId
JOIN [YARA].[Incident] AS i ON a.incidentId = i.incidentId
GROUP BY o.officerId, o.officerName, YEAR(i.incidentDate)
ORDER BY [TotalIncidents] DESC;
GO

-- 4) All persons arrested on 2025-09-20
SELECT 
    p.personSSN, 
    p.personName, 
    p.personPhoneNumber,
    a.arrestId, 
    a.arrestDate, 
    a.arrestLocation, 
    a.arrestStatus
FROM [YARA].[Person] AS p
JOIN [YARA].[Arrest] AS a ON p.personSSN = a.personSSN
WHERE CAST(a.arrestDate AS DATE) = '2025-09-20'
AND a.arrestStatus = 'Arrested';
GO
Select * 
From [YARA].[Person] i
WHERE i.personName LIKE 'Yash'