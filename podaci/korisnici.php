<?php
	$contentType = "";
	if (isset($_GET['contentType'])) {
		$contentType = $_GET['contentType'];
	}
	
	if ($contentType == 'xml') {	
		header("Content-Type:application/xml");
		echo '<?xml version="1.0" encoding="utf-8"?><korisnici>';
	} else if ($contentType == 'json') {
		header("Content-Type:application/json");
	} else {
		die('Nepoznat tip podataka');
	}
	
	$conn = new mysqli("localhost", "root","","webdip2010") or die(mysqli_error());
	
	
	$conn->set_charset('utf8');
	
	$result = $conn->query("SELECT * FROM korisnik");
	
	if($result){
		 // Cycle through results
		 $korisnici = array();
		while ($korisnik = $result->fetch_object()){
			//echo $korisnik->ime . "<br>";
			$korisnici[] = $korisnik;
		}
		
		if ($contentType == 'json') {
			echo json_encode($korisnici);
		} else {
			foreach($korisnici as $korisnik) {
				echo "<korisnik ";
				foreach(get_object_vars($korisnik) as $k => $v) {
					echo $k . "='$v' ";
				}
				echo "/>";
				/*echo "<korisnik id='{$korisnik->id_korisnik}' ime='{$korisnik->ime}' prezime='{$korisnik->prezime}' 
					korisnicko_ime='{$korisnik->korisnicko_ime}'/>";*/
			}
		}
		// Free result set
		$result->close();
		
	}

	
	if ($contentType == 'xml') {	
		echo "</korisnici>";
	}
	
	
	
?>