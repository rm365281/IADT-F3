-- ============================================================
-- ============================================================
--  TABLE: patients
-- ============================================================
CREATE TABLE patients (
    id              CHAR(36) PRIMARY KEY COMMENT 'UUID do paciente',
    full_name       VARCHAR(255) NOT NULL COMMENT 'Full name of the patient',
    birth_date      DATE COMMENT 'Date of birth',
    gender          ENUM('male','female','other') COMMENT 'Patient gender',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
                        ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update',

    INDEX idx_full_name (full_name),
    INDEX idx_birth_date (birth_date)
) COMMENT='Master table containing patient registration data';


-- ============================================================
-- ============================================================
--  TABLE: exams_available
-- ============================================================
CREATE TABLE exams_available (
    id              CHAR(36) PRIMARY KEY COMMENT 'UUID do tipo de exame',
    name            VARCHAR(255) NOT NULL COMMENT 'Exam name',
    description     TEXT COMMENT 'Detailed description of the exam',
    preparation     TEXT COMMENT 'Preparation instructions',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',

    INDEX idx_name (name)
) COMMENT='Catalog of exams available at the hospital';


-- ============================================================
-- ============================================================
--  TABLE: exam_scheduling (PARTITIONED BY YEAR OF SCHEDULED DATE)
-- ============================================================
CREATE TABLE exam_scheduling (
    id              CHAR(36) PRIMARY KEY COMMENT 'UUID do agendamento',
    patient_id      CHAR(36) NOT NULL COMMENT 'Associated patient',
    exam_id         CHAR(36) NOT NULL COMMENT 'Type of scheduled exam',
    scheduled_at    DATETIME NOT NULL COMMENT 'Scheduled date and time',
    status          ENUM('scheduled','in_progress','completed','cancelled') NOT NULL 
                        COMMENT 'Current scheduling status',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',

    INDEX idx_patient_id (patient_id),
    INDEX idx_exam_id (exam_id),
    INDEX idx_scheduled_at (scheduled_at),

    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (exam_id) REFERENCES exams_available(id)
)
COMMENT='Exam appointments by patient'
PARTITION BY RANGE (YEAR(scheduled_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);


-- ============================================================
-- ============================================================
--  TABLE: exam_results (PARTITIONED BY YEAR OF RESULT)
-- ============================================================
CREATE TABLE exam_results (
    id                  CHAR(36) PRIMARY KEY COMMENT 'UUID do resultado do exame',
    exam_schedule_id    CHAR(36) NOT NULL COMMENT 'Exam schedule',
    result_text         TEXT COMMENT 'Result text',
    result_file_url     VARCHAR(500) COMMENT 'URL of the PDF or image file',
    result_date         DATETIME NOT NULL COMMENT 'Exam completion date',
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',

    INDEX idx_exam_schedule_id (exam_schedule_id),
    INDEX idx_result_date (result_date),

    FOREIGN KEY (exam_schedule_id) REFERENCES exam_scheduling(id)
)
COMMENT='Results of exams performed on patients'
PARTITION BY RANGE (YEAR(result_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);


-- ============================================================
-- ============================================================
--  TABLE: health_history (PARTITIONED BY YEAR OF EVENT)
-- ============================================================
CREATE TABLE health_history (
    id              CHAR(36) PRIMARY KEY COMMENT 'UUID do registro histórico',
    patient_id      CHAR(36) NOT NULL COMMENT 'Linked patient',
    title           VARCHAR(255) NOT NULL COMMENT 'Health event title',
    description     TEXT NOT NULL COMMENT 'Event description',
    occurred_at     DATETIME COMMENT 'Date of clinical event',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',

    INDEX idx_patient_id (patient_id),
    INDEX idx_occurred_at (occurred_at),

    FOREIGN KEY (patient_id) REFERENCES patients(id)
)
COMMENT='Detailed clinical history of each patient'
PARTITION BY RANGE (YEAR(occurred_at)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);


-- ============================================================
-- ============================================================
--  TABLE: old_health_reports (PARTITIONED BY YEAR OF REPORT)
-- ============================================================
CREATE TABLE old_health_reports (
    id              CHAR(36) PRIMARY KEY COMMENT 'UUID do relatório antigo',
    patient_id      CHAR(36) NOT NULL COMMENT 'Linked patient',
    file_url        VARCHAR(500) NOT NULL COMMENT 'URL of the old file',
    report_type     VARCHAR(255) COMMENT 'Report type',
    report_date     DATE COMMENT 'Original report date',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date',

    INDEX idx_patient_id (patient_id),
    INDEX idx_report_date (report_date),

    FOREIGN KEY (patient_id) REFERENCES patients(id)
)
COMMENT='Digitized old medical reports'
PARTITION BY RANGE (YEAR(report_date)) (
    PARTITION p2010 VALUES LESS THAN (2011),
    PARTITION p2015 VALUES LESS THAN (2016),
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
-- ============================================================
