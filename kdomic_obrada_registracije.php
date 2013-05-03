<?php session_start(); ?>
<?php

?>
<?php
	if(isset($_GET['potvrda'])){
		require_once("privatno/korisnici.php");
		$database = new KorisnikBAZA(); 
		$korisnici = $database->find_by_sql("SELECT * FROM korisnici WHERE email_potvrda='".$_GET['potvrda']."'");
		$korisnici = array_pop($korisnici);
		if(!$korisnici) {
			echo "Korisni&#269;ki ra&#269;un je ve&#263; aktiviran!";
		} else {
			$exp_date = date('Y-m-d H:i:s', strtotime('+1 day', strtotime($korisnici['datum_registracije'])));
			$todays_date = date("Y-m-d H:i:s");
			$today = strtotime($todays_date);
			$expiration_date = strtotime($exp_date);
			if($expiration_date > $today){
				$korisnici['email_potvrda'] = 'aktiviran';
				$data = array();
				foreach ($korisnici as $key => $value)
					$data[] = "{$key}='{$value}'";				
				$sql  = "UPDATE korisnici SET " . join(", ", $data);
				$sql .= " WHERE id={$korisnici['id']}";
				$database->update_by_sql($sql);
				echo "Aktivirano!";
			} else { 
				echo "Vrijeme za registraciju isteklo";
			}
		}		
	} else {
		if($_POST['captcha']!=$_SESSION['captcha']){
			header('Location: kdomic_register.php?error=1');
			exit();
		}
		preg_match('/[a-zA-Z0-9]{3,}@foi.hr/', $_POST['email'], $matches);
		if(!$matches){
			header('Location: kdomic_register.php?error=2');
			exit();
		}
		require_once("privatno/korisnici.php");		
		$database = new KorisnikBAZA();
		$email_potvrda = md5(uniqid(rand(), true));
		$query  = "INSERT INTO korisnici ";
		$query .= " (`ime`,`prezime`,`email`,`password`,`mjesto`,`telefon`,`email_potvrda`,`datum_registracije`) VALUES ";
		$query .= " ('".$_POST['ime']."','".$_POST['prezime']."','".$_POST['email']."','".sha1($_POST['lozinka'])."','".$_POST['mjesto']."','".$_POST['telefon']."', '".$email_potvrda."','".date("Y-m-d H:i:s")."') ";
	    $korisnici = $database->insert_by_sql($query);

		$to = $_POST['email'];
		$subject = "Registracija";
		$message  =	'Aktiviraj se: ';
		$message .= 'http://arka.foi.hr/WebDiP/2012/vjezba_05/kdomic/kdomic_obrada_registracije.php?potvrda='.$email_potvrda;
		$from = "kdomic@foi.hr";
		$headers = "From:" . $from;
		mail($to,$subject,$message,$headers);
	    echo "Unos pohranjen! <br> Provjerite e-mail radi potvrde!";
	}
	echo " <br> <a href=kdomic_index.html>Nazad</a>";


?>


