<?php
	$captcha = "";
	for ($i=0; $i < 5; $i++)
		$captcha .= chr(rand(97,122));
	$image = imagecreatetruecolor(170, 60);
	$txt = imagecolorallocate($image, 255, 10, 10);
	$back = imagecolorallocate($image, 255, 255, 255);
	imagefilledrectangle($image, 0, 0, 200, 100, $back);
	imagettftext($image, 30, 5, 10, 40, $txt, "fonts/MankSans.ttf", $captcha);
	Header("Content-Type: image/png");
	imagepng($image);
?>