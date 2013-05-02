<?php

	class KorisnikJSON {
		public static function dajSve()
		{
			$_json = json_decode(file_get_contents('podaci/korisnici_novi.json'),true);
			$json = array();
			foreach ($_json as $value){
				$key = (int)$value['id_korisnik'];
				$json[$key] = $value;
			}
			return $json;
		}

		public static function dajKorisnika($id)
		{
			$svi = self::dajSve();
			return $svi[$id];
		}

		public static function spremi($korisnik){
			$svi = self::dajSve();
			$id = $korisnik['id_korisnik'];
			unset($korisnik['spremi']);
			foreach ($korisnik as $key => $value) {
				$svi[$id][$key] = $value;
			}
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			header('Location: kdomic_tablica.php');
		}

		public static function obrisi($korisnik){
			$svi = self::dajSve();
			$id = $korisnik['id_korisnik'];
			unset($svi[$id]);
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			header('Location: kdomic_tablica.php');
		}

		public static function novi($korisnik){
			$svi = self::dajSve();
			$id = $svi[count($svi)]['id_korisnik']+1;
			$korisnik['id_korisnik'] = $id;
			unset($korisnik['novi']);			
			array_push($svi, $korisnik);
			file_put_contents('podaci/korisnici_novi.json', json_encode($svi));
			print_r($korisnik);
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
