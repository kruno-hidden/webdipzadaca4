<pre>
<?php

	class KorisnikJSON {
		public static function dajSve()
		{
			return json_decode(file_get_contents('podaci/korisnici_novi.json'),true);
		}

		public static function dajKorisnika($id)
		{
			$svi = self::dajSve();
			return $svi[$id];
		}
	}
?>
</pre>