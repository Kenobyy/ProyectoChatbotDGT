
-- SNOWFLAKE
-- Pregutas:

-- ¿Cuántos vehículos se matricularon en el 2023 en España?
SELECT BRAND_NAME, COUNT(*) AS total_registrations_2022 
FROM PAUL_MATRICULACIONES.MATRICULACIONES.MATRICULACIONES 
WHERE REGISTRATION_DATE BETWEEN '2023-01-01' AND '2023-12-31' BY BRAND_NAME 
ORDER BY total_registrations_ciudad_real DESC

-- ¿Cuál es la marca con más matriculaciones en España?
SELECT BRAND_NAME, COUNT(*) AS total_registrations 
FROM PAUL_MATRICULACIONES.MATRICULACIONES.MATRICULACIONES 
GROUP BY BRAND_NAME 
ORDER BY total_registrations DESC

-- ¿Cuál es la marca con más matriculaciones en la provincia de Ciudad Real?
SELECT BRAND_NAME, COUNT(*) AS total_registrations_ciudad_real 
FROM PAUL_MATRICULACIONES.MATRICULACIONES.MATRICULACIONES 
WHERE PROVINCE_REGISTRATION = 'CIUDAD REAL' 
GROUP BY BRAND_NAME 
ORDER BY total_registrations_ciudad_real DESC

-- ¿Cuál es la provincia con más matriculaciones en el mes de septiembre de 2022?
SELECT PROVINCE_REGISTRATION, COUNT(*) AS total_registrations_september_2022
FROM PAUL_MATRICULACIONES.MATRICULACIONES.MATRICULACIONES
WHERE EXTRACT(MONTH FROM REGISTRATION_DATE) = 9 AND EXTRACT(YEAR FROM REGISTRATION_DATE) = 2022
GROUP BY PROVINCE_REGISTRATION
ORDER BY total_registrations_september_2022 DESC LIMIT 5;

-- ¿Cuáles son los 5 modelos con más matriculaciones en España?
SELECT MODEL_NAME, COUNT(*) AS total_registrations 
FROM PAUL_MATRICULACIONES.MATRICULACIONES.MATRICULACIONES 
GROUP BY MODEL_NAME 
ORDER BY total_registrations DESC LIMIT 5;