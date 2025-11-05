INSERT INTO patients (id, full_name, birth_date, gender)
VALUES
(UUID(), 'Alice Souza', '1988-04-12', 'female'),
(UUID(), 'Bruno Ribeiro', '1991-07-30', 'male'),
(UUID(), 'Carla Oliveira', '1979-01-22', 'female'),
(UUID(), 'Daniel Fernandes', '1985-11-19', 'male'),
(UUID(), 'Elisa Martins', '1996-05-03', 'female'),
(UUID(), 'Felipe Costa', '1989-09-14', 'male'),
(UUID(), 'Gabriela Rocha', '1993-02-11', 'female'),
(UUID(), 'Henrique Duarte', '1981-03-07', 'male'),
(UUID(), 'Isabela Freitas', '1999-10-27', 'female'),
(UUID(), 'João Mendes', '1975-12-09', 'male'),
(UUID(), 'Karina Lopes', '1997-06-17', 'female'),
(UUID(), 'Leonardo Araújo', '1984-08-25', 'male'),
(UUID(), 'Mariana Torres', '1992-09-12', 'female'),
(UUID(), 'Nicolas Prado', '2000-03-11', 'male'),
(UUID(), 'Olívia Albuquerque', '1987-04-05', 'female'),
(UUID(), 'Paulo Vieira', '1973-07-19', 'male'),
(UUID(), 'Queila Santos', '2001-11-01', 'female'),
(UUID(), 'Rafael Lima', '1994-12-22', 'male'),
(UUID(), 'Sabrina Castro', '1986-05-13', 'female'),
(UUID(), 'Thiago Barros', '1991-09-12', 'male'),
(UUID(), 'Ursula Andrade', '1983-03-22', 'female'),
(UUID(), 'Vitor Carvalho', '1997-08-15', 'male'),
(UUID(), 'Wesley Peixoto', '1985-10-04', 'male'),
(UUID(), 'Xênia Pinheiro', '1999-01-14', 'female'),
(UUID(), 'Yuri Tavares', '2002-06-29', 'male');

INSERT INTO exams_available (id, name, description, preparation)
VALUES
(UUID(), 'Hemograma Completo', 'Avaliação geral da saúde.', 'Jejum não necessário.'),
(UUID(), 'Raio-X Tórax', 'Imagem da caixa torácica.', 'Remover objetos metálicos.'),
(UUID(), 'Ressonância Magnética', 'Imagem detalhada de tecidos.', 'Jejum de 4 horas.'),
(UUID(), 'Ultrassom Abdominal', 'Imagem dos órgãos abdominais.', 'Jejum de 8 horas.'),
(UUID(), 'Eletrocardiograma', 'Atividade elétrica do coração.', 'Evitar atividade física intensa.');

INSERT INTO exam_scheduling (id, patient_id, exam_id, scheduled_at, status)
SELECT UUID(), p.id, e.id,
       DATE_ADD('2024-01-01', INTERVAL (ROW_NUMBER() OVER()) DAY),
       'completed'
FROM patients p
CROSS JOIN (SELECT id FROM exams_available ORDER BY created_at LIMIT 1) e
LIMIT 25;

INSERT INTO exam_results (id, exam_schedule_id, result_text, result_file_url, result_date)
SELECT UUID(),
       es.id,
       CONCAT('Resultado normal para o paciente ', p.full_name),
       CONCAT('https://files.hospital.com/results/', es.id, '.pdf'),
       DATE_ADD(es.scheduled_at, INTERVAL 1 DAY)
FROM exam_scheduling es
JOIN patients p ON p.id = es.patient_id;

INSERT INTO health_history (id, patient_id, title, description, occurred_at)
SELECT
    UUID(),
    p.id,
    ev.title,
    ev.description,
    DATE_ADD('2023-01-01', INTERVAL FLOOR(RAND()*365) DAY)
FROM patients p
CROSS JOIN (
    SELECT 'Consulta de rotina' AS title, 'Exame anual sem alterações.' AS description
    UNION ALL SELECT 'Gripe', 'Sintomas leves tratados com repouso.'
    UNION ALL SELECT 'Dor de cabeça', 'Cefaleia tensional, sem gravidade.'
) ev;
