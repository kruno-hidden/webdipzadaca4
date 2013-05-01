<?php
    
    defined('DB_SERVER') ? null : define("DB_SERVER", "localhost");
    defined('DB_USER')   ? null : define("DB_USER", "root");
    defined('DB_PASS')   ? null : define("DB_PASS", "");
    defined('DB_NAME')   ? null : define("DB_NAME", "WebDiP2012_013");
	
	class KorisnikBAZA extends mysqli{

        private $connection;		

		function __construct() {
			$connection = false;
	        parent::__construct(DB_SERVER, DB_USER, DB_PASS, DB_NAME);
	        if(mysqli_connect_error())
	            die( 'Connect Error (' . mysqli_connect_errno() . ') ' . mysqli_connect_error() );
            $connection = true;	        
		}

		public function db_close_connection() {		
            if($this->connection) {
                $this->close();
                $this->connection=false;
            }
        }

        public function find_by_sql($sql="") {
        	$result = $this->query($sql);
        	$dataSet = array();
        	while ($row = $result->fetch_array(MYSQLI_ASSOC)) {
        		$dataSet[] = $row;
        	}
        	return $dataSet;
        }        
	}
    $database = new KorisnikBAZA();	
    echo "<table id=sviKorisnici>";
    echo "<thead>";
		echo "<tr><td>ID</td><td>Ime</td><td>Prezime</td><td>Korisničko</td><td>Lozinka</td></tr>";
    echo "</thead>";
    echo "<tbody>";
    $korisnici = $database->find_by_sql("SELECT * FROM korisnici");
    foreach ($korisnici as $korisnik) {
    	echo '<tr>';
    		echo '<td>'.$korisnik['id'].'</td>';
    		echo '<td>'.$korisnik['ime'].'</td>';
    		echo '<td>'.$korisnik['prezime'].'</td>';
    		echo '<td>'.$korisnik['email'].'</td>';
    		echo '<td>'.$korisnik['lozinka'].'</td>';    		
    	echo '</tr>';    	
    }

/*
    
    foreach ($svi as $korisnik) {
        echo "<tr>";
        foreach ($korisnik as $key => $atribut) {
            if($key=="slika") continue;
            echo "<td>".$atribut."</td>";        
        }
        echo "</tr>";                    
    }
    echo "</tbody>";                    
    echo "</table>";
*/

?>	