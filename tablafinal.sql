-- Query correspondiente a la modificación de la columna FEC_MATRICULA en formato DATE.

SELECT
   *,
    FEC_MATRICULA,
    
    CONVERT(
        DATE,
        SUBSTRING(FEC_MATRICULA, 5, 4) +    
        SUBSTRING(FEC_MATRICULA, 3, 2) +    
        SUBSTRING(FEC_MATRICULA, 1, 2),     
        112                                 
    ) AS Registration_Date
FROM
    matriculaciones_2021_2023

-- Query correspondiente a la limpieza de los campos.

SELECT
    -- Elimina registros donde FEC_MATRICULA esté vacío o contenga caracteres especiales
    NULLIF(FEC_MATRICULA, '') AS FEC_MATRICULA,
    CASE 
        WHEN PATINDEX('%[^a-zA-Z0-9 ]%', FEC_MATRICULA) = 0 THEN FEC_MATRICULA
        ELSE NULL
    END AS FEC_MATRICULA_CLEAN,

    -- Elimina registros donde MARCA esté vacío o contenga caracteres especiales
    NULLIF(MARCA, '') AS MARCA,
    CASE 
        WHEN PATINDEX('%[^a-zA-Z0-9 ]%', MARCA) = 0 THEN MARCA
        ELSE NULL
    END AS MARCA_CLEAN,
    
    -- Elimina registros donde MODELO esté vacío o contenga caracteres especiales
    NULLIF(MODELO, '') AS MODELO,
    CASE 
        WHEN PATINDEX('%[^a-zA-Z0-9 ]%', MODELO) = 0 THEN MODELO
        ELSE NULL
    END AS MODELO_CLEAN,

    -- Elimina registros donde COD_PROVINCIA esté vacío o contenga caracteres especiales
    NULLIF(COD_PROVINCIA_VEH, '') AS COD_PROVINCIA_VEH,
    CASE 
        WHEN PATINDEX('%[^a-zA-Z0-9 ]%', COD_PROVINCIA_VEH) = 0 THEN COD_PROVINCIA_VEH
        ELSE NULL
    END AS COD_PROVINCIA_CLEAN

-- Query correspondiente a la realización de un JOIN con de la tabla provincias y renombre de los campos.
SELECT
   
    t.FEC_MATRICULA AS Registration_Date,
    t.MARCA_CLEAN AS Brand_Name],
    t.MODELO_CLEAN AS Model_Name,
    p.Province_Registration
FROM
   
    matriculaciones_top1000 AS t
INNER JOIN
    provincias AS p
    ON t.COD_PROVINCIA_VEH = p.COD_PROVINCIA_VEH
WHERE
    t.FEC_MATRICULA NOT LIKE '%[^0-9]%' AND 
    t.MARCA NOT LIKE '%[^a-zA-Z0-9]%' AND   
    t.MODELO NOT LIKE '%[^a-zA-Z0-9]%' AND  
    t.COD_PROVINCIA_VEH NOT LIKE '%[^0-9]%';   

.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-..-.--.-.-..-.-.-.-..--..-.-.-.-.-.-..-.-..-.-.-.-..


SNOWFLAKE

pregutas:
¿Cuántos vehículos se matricularon en el 2021 en España?

SELECT COUNT(*) AS total_vehicles_2021 
FROM PAUL
WHERE REGISTRATION_DATE BETWEEN '20210101' AND '20211231';


¿Cuál es la marca con más matriculaciones en España?

SELECT BRAND_NAME, COUNT(*) AS total_registrations 
FROM PAUL
GROUP BY BRAND_NAME ORDER BY total_registrations DESC

¿Cuál es la marca con más matricualciones en la provincia de CIUDAD REAL?
SELECT  BRAND_NAME, COUNT(*) AS total_registrations_ciudad_real 
FROM matriculaciones_2021_2023
WHERE province_Registration = 'CIUDAD REAL'
GROUP BY BRAND_NAME ORDER BY total_registrations_ciudad_real DESC
