<?php

	class KorisnikJSON {
		public static function dajSve()
		{
			return json_decode(file_get_contents('podaci/korisnici_novi.json'),true);
		}

		public static function dajKorisnika($id)
		{
			$svi = self::dajSve();
			return $svi[$id-1];
		}

		public static function spremi($korisnik){
			$svi = self::dajSve();
			$id = $korisnik['id_korisnik']-1;
			unset($korisnik['spremi']);
			foreach ($korisnik as $key => $value) {
				$svi[$id][$key] = $value;
			}
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			header('Location: kdomic_tablica.php');
		}

		public static function obrisi($korisnik){
			$svi = self::dajSve();
			$id = $korisnik['id_korisnik']-1;
			unset($svi[$id]);
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			header('Location: kdomic_tablica.php');
		}

		public static function novi($korisnik){
			$svi = self::dajSve();
			$id = $svi[count($svi)-1]['id_korisnik']+1;
			$korisnik['id_korisnik'] = $id;
			unset($korisnik['spremi']);			
			array_push($svi, $korisnik);
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			header('Location: kdomic_tablica.php');
		}

	}

	if(isset($_POST['spremi'])){
		KorisnikJSON::spremi($_POST);
	}

	if(isset($_POST['obrisi'])){
		KorisnikJSON::obrisi($_POST);
	}

	if(isset($_POST['novi'])){
		KorisnikJSON::novi($_POST);
	}
?>
