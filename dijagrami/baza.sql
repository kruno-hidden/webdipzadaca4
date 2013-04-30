SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';


-- -----------------------------------------------------
-- Table `korisnici`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `korisnici` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `ime` VARCHAR(45) NOT NULL ,
  `prezime` VARCHAR(45) NOT NULL ,
  `adresa` VARCHAR(45) NOT NULL ,
  `pbr` VARCHAR(5) NOT NULL ,
  `mjesto` VARCHAR(45) NOT NULL ,
  `telefon` VARCHAR(20) NULL ,
  `email` VARCHAR(45) NOT NULL ,
  `oib` VARCHAR(11) NOT NULL ,
  `open_id` MEDIUMINT(9) NULL DEFAULT 0 COMMENT '0 - normalno\n1- facebook\n2 - google' ,
  `opomena` MEDIUMINT(9) NULL DEFAULT 0 COMMENT 'Brojanje opomena nakon trece ide deakrtivacija' ,
  `deaktiviran` TINYINT(4) NULL DEFAULT 0 COMMENT '0 aktiviran\n1 deaktiviran' ,
  `zamrznut` DATETIME NULL COMMENT 'Datum do kojeg je aktiviran' ,
  `blokiran` TINYINT(4) NULL COMMENT '0  nije\n1 blokiran' ,
  `datum_registracije` DATETIME NULL ,
  `email_potvrda` VARCHAR(45) NULL ,
  `username` VARCHAR(45) NOT NULL ,
  `password` VARCHAR(45) NOT NULL ,
  `ovlasti` MEDIUMINT(9) NOT NULL COMMENT '1 reg_user\n2 mod\n3 admin' ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `kategorije`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `kategorije` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `naziv` VARCHAR(45) NOT NULL ,
  `aktivna` TINYINT(4) NOT NULL DEFAULT 1 COMMENT '0 neaktivna\n1 aktivna' ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `moderatori`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `moderatori` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `id_kategorije` INT NOT NULL ,
  `aktivan` TINYINT(4) NOT NULL COMMENT '0 nema mogucnost moderiranja\n1 ima' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_moderatori_1` (`id_korisnika` ASC) ,
  INDEX `fk_moderatori_2` (`id_kategorije` ASC) ,
  CONSTRAINT `fk_moderatori_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_moderatori_2`
    FOREIGN KEY (`id_kategorije` )
    REFERENCES `kategorije` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `opomene`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `opomene` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `id_moderatora` INT NOT NULL ,
  `datum` DATETIME NOT NULL ,
  `opis` TEXT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_opomene_1` (`id_korisnika` ASC) ,
  INDEX `fk_opomene_2` (`id_moderatora` ASC) ,
  CONSTRAINT `fk_opomene_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_opomene_2`
    FOREIGN KEY (`id_moderatora` )
    REFERENCES `korisnici` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `newsletter`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `newsletter` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `aktivan` TINYINT(4) NOT NULL COMMENT '0 neaktivan\n1 aktivan' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_newsletter_1` (`id_korisnika` ASC) ,
  CONSTRAINT `fk_newsletter_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `prodavatelji`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `prodavatelji` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL COMMENT 'korisnik koji je zaduzen za to poduc+zece' ,
  `naziv` VARCHAR(45) NOT NULL ,
  `adresa` VARCHAR(45) NOT NULL ,
  `kontakt` VARCHAR(15) NOT NULL ,
  `info` VARCHAR(45) NOT NULL ,
  `oib` VARCHAR(45) NOT NULL ,
  `aktivan` TINYINT(4) NOT NULL COMMENT '0 neaktivan\n1 aktivan' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_prodavatelji_1` (`id_korisnika` ASC) ,
  CONSTRAINT `fk_prodavatelji_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ponude`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `ponude` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_prodavatelja` INT NOT NULL ,
  `id_kategorije` INT NOT NULL ,
  `naslov` TEXT NOT NULL ,
  `podnaslov` TEXT NOT NULL ,
  `cijena` FLOAT NOT NULL ,
  `opis_naslov` TEXT NOT NULL ,
  `opis_kratki` TEXT NOT NULL ,
  `opis` TEXT NOT NULL ,
  `napomena` VARCHAR(45) NOT NULL ,
  `karta_x` VARCHAR(45) NULL ,
  `karta_y` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_ponude_1` (`id_prodavatelja` ASC) ,
  INDEX `fk_ponude_2` (`id_kategorije` ASC) ,
  CONSTRAINT `fk_ponude_1`
    FOREIGN KEY (`id_prodavatelja` )
    REFERENCES `prodavatelji` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ponude_2`
    FOREIGN KEY (`id_kategorije` )
    REFERENCES `kategorije` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `akcije`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `akcije` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_ponude` INT NOT NULL ,
  `popust` INT NOT NULL ,
  `datum_pocetka` DATETIME NOT NULL ,
  `datum_zavrsetka` DATETIME NOT NULL ,
  `limit` INT NOT NULL ,
  `istaknuto` TINYINT(4) NULL DEFAULT 0 COMMENT '0 ne\n1 da' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_akcije_1` (`id_ponude` ASC) ,
  CONSTRAINT `fk_akcije_1`
    FOREIGN KEY (`id_ponude` )
    REFERENCES `ponude` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `kosarica`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `kosarica` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `id_akcije` INT NOT NULL ,
  `operacija` MEDIUMINT(9) NOT NULL DEFAULT 0 COMMENT '0 dodano\n1 izbaceno\n2 kupljeno' ,
  `datum` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_kosarica_1` (`id_korisnika` ASC) ,
  INDEX `fk_kosarica_2` (`id_akcije` ASC) ,
  CONSTRAINT `fk_kosarica_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_kosarica_2`
    FOREIGN KEY (`id_akcije` )
    REFERENCES `akcije` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `log_tip`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `log_tip` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `opis` TEXT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `logovi`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `logovi` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `id_tip` INT NOT NULL COMMENT 'tip zapisa' ,
  `kljuc` INT NOT NULL ,
  `datum` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_logovi_1` (`id_korisnika` ASC) ,
  INDEX `fk_logovi_2` (`id_tip` ASC) ,
  CONSTRAINT `fk_logovi_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_logovi_2`
    FOREIGN KEY (`id_tip` )
    REFERENCES `log_tip` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `racuni`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `racuni` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `datum` DATETIME NOT NULL ,
  `placeno` TINYINT(4) NOT NULL COMMENT '0 ne\n1 da' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_racuni_1` (`id_korisnika` ASC) ,
  CONSTRAINT `fk_racuni_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `vaucheri`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `vaucheri` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `ime` VARCHAR(45) NOT NULL ,
  `email` VARCHAR(45) NOT NULL ,
  `poruka` TEXT NOT NULL ,
  `vrijednost` INT NOT NULL ,
  `id_racuna` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vaucheri_1` (`id_korisnika` ASC) ,
  INDEX `fk_vaucheri_2` (`id_racuna` ASC) ,
  CONSTRAINT `fk_vaucheri_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_vaucheri_2`
    FOREIGN KEY (`id_racuna` )
    REFERENCES `racuni` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `komentari`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `komentari` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_korisnika` INT NOT NULL ,
  `id_ponude` INT NOT NULL ,
  `komentar` TEXT NOT NULL ,
  `datum` DATETIME NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_komentari_1` (`id_korisnika` ASC) ,
  INDEX `fk_komentari_2` (`id_ponude` ASC) ,
  CONSTRAINT `fk_komentari_1`
    FOREIGN KEY (`id_korisnika` )
    REFERENCES `korisnici` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_komentari_2`
    FOREIGN KEY (`id_ponude` )
    REFERENCES `ponude` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `racuni_akcije`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `racuni_akcije` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_racuna` INT NOT NULL ,
  `id_akcije` INT NOT NULL ,
  `kolicina` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_racuni_akcije_1` (`id_racuna` ASC) ,
  INDEX `fk_racuni_akcije_2` (`id_akcije` ASC) ,
  CONSTRAINT `fk_racuni_akcije_1`
    FOREIGN KEY (`id_racuna` )
    REFERENCES `racuni` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_racuni_akcije_2`
    FOREIGN KEY (`id_akcije` )
    REFERENCES `akcije` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `gradovi`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `gradovi` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `ime` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gradovi_akcije`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `gradovi_akcije` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `id_grada` INT NOT NULL ,
  `id_akcije` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_gradovi_akcije_1` (`id_grada` ASC) ,
  INDEX `fk_gradovi_akcije_2` (`id_akcije` ASC) ,
  CONSTRAINT `fk_gradovi_akcije_1`
    FOREIGN KEY (`id_grada` )
    REFERENCES `gradovi` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_gradovi_akcije_2`
    FOREIGN KEY (`id_akcije` )
    REFERENCES `akcije` (`id` )
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
