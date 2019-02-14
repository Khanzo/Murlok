CREATE TABLE `habr` (
  `id` INTEGER PRIMARY KEY,
  `published` INTEGER NOT NULL,
  `title` TEXT,
  `url_post` TEXT,
  `date` TEXT,
  `avtor` TEXT,
  `cashe` TEXT NOT NULL UNIQUE
)