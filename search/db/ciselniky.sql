CREATE TABLE cl_vzdelani_detailni_kategorie (
                                                id VARCHAR(20) PRIMARY KEY,
                                                nazev VARCHAR(50)
);

INSERT INTO cl_vzdelani_detailni_kategorie (id, nazev) VALUES
                                                           ('nizsiStred', 'Nižší střední'),
                                                           ('usv', 'Ukončené střední vzdělání'),
                                                           ('stredOdbor', 'Střední odborné'),
                                                           ('neuplZakl', 'Neúplné základní'),
                                                           ('nizsiStredOdbor', 'Nižší střední odborné'),
                                                           ('zaklPraktSkol', 'Základní praktická škola'),
                                                           ('usoSMat', 'Střední s maturitou'),
                                                           ('stredOdborVyuc', 'Střední odborné s výučním listem'),
                                                           ('vyssOdbor', 'Vyšší odborné'),
                                                           ('konz', 'Konzervatoř'),
                                                           ('doktor', 'Doktorské studium'),
                                                           ('bakal', 'Bakalářské studium'),
                                                           ('vysoka', 'Vysokoškolské'),
                                                           ('usoSMatVyuc', 'Střední s maturitou a výučním listem'),
                                                           ('bezVzdel', 'Bez vzdělání');

CREATE TABLE cl_pracovnepravni_vztah (
                                         id VARCHAR(20) PRIMARY KEY,
                                         nazev VARCHAR(50)
);

INSERT INTO cl_pracovnepravni_vztah (id, nazev) VALUES
                                                    ('sluzebni', 'Služební poměr'),
                                                    ('dpc', 'Dohoda o pracovní činnosti'),
                                                    ('zkraceny', 'Zkrácený úvazek'),
                                                    ('dpp', 'Dohoda o provedení práce'),
                                                    ('plny', 'Plný úvazek');

