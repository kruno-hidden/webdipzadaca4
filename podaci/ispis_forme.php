<html>
	<head>
		<meta charset="utf-8"/>
	</head>
	<body>
<?php

if($_POST) {
	echo "Primljeni podaci: <hr/>";
	foreach($_POST as $k=>$v) {
		echo $k . "=". $v . "<br/>";
	}
} else {
	echo "Podaci moraju biti poslani HTTP POST metodom";
}

?>
</body>
</html>
