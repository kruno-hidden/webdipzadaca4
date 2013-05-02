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

        public function insert_by_sql($sql="") {
            return $this->query($sql);
        }

        public function update_by_sql($sql="") {
            return $this->query($sql);
        }

	}
?>	