<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="../css/kdomic_main.css" />
        <link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.css" />        
        <script type="text/javascript" src="../js/jquery.min.js"></script>
        <script type="text/javascript" src="../js/jquery.dataTables.js"></script>        
        <script type="text/javascript" src="../js/kdomic_main.js"></script>        
    </head>

    <body>
        <div id="outerDiv">
            <header>
                <nav id="mainMenu">
                    <ul>
                        <li><a href="../kdomic_index.html">Početna</a></li>                        
                        <li><a href="../kdomic_register.php">Registracija</a></li>
                        <li><a href="../kdomic_login.html">Prijava</a></li>
                        <li><a href="../kdomic_tablica.php" >Tablica</a></li>
                        <li><a href="../kdomic_dijagrami.html">Dijagrami</a></li>
                        <li><a href="kdomic_ispis.php" class="current">Privatno</a></li>                        
                    </ul>
                </nav>
                <h1>Krunoslav Domić </h1>
            </header>

            <div class="subMenu"> </div>

            <section>
            <?php 
                require("korisnici.php");
                $database = new KorisnikBAZA();
                if(isset($_POST['submit'])):                    
                    $data = array();
                    array_pop($_POST);
                    foreach ($_POST as $key => $value)
                        $data[] = "{$key}='{$value}'";              
                    $sql  = "UPDATE korisnici SET " . join(", ", $data);
                    $sql .= " WHERE id={$_POST['id']}";
                    $database->update_by_sql($sql);
                endif;
                if(isset($_GET['id'])):   
                    $korisnici = $database->find_by_sql("SELECT * FROM korisnici WHERE id=".$_GET['id']);
                    $korisnik = array_pop($korisnici);
            ?>
                <form action="kdomic_ispis.php" method="POST" autocomplete="off">
                        <input type="hidden" name="id" value="<?php echo $korisnik['id']; ?>" />
                    <table class="register">
                        <tr>
                            <td><label for="ime">Ime</label></td>
                            <td><input type="text" name="ime" id="ime" required placeholder="Vaše ime" autofocus value="<?php echo $korisnik['ime'] ?>"/></td>
                        </tr>
                        <tr>
                            <td><label for="prezime">Prezime</label></td>
                            <td><input type="text" name="prezime" id="prezime" required placeholder="Vaše prezime" value="<?php echo $korisnik['prezime'] ?>"/></td>
                        </tr>
                        <tr>
                            <td><label for="email">Email</label></td>
                            <td><input type="email" name="email" id="email" pattern="[a-zA-Z0-9]{3,}@foi.hr" required placeholder="nesto@foi.hr" value="<?php echo $korisnik['email'] ?>" /></td>
                        </tr>
                        <tr>
                            <td><label for="lozinka">Lozinka</label></td>
                            <td><input type="password" name="password" id="password"  pattern="[a-zA-Z0-9]{6,}" required placeholder="Lozinka" value="<?php echo $korisnik['password'] ?>"/></td>
                        </tr>
                        <tr>
                            <td><label for="telefon">Broj telefona</label></td>
                            <td><input type="tel" name="telefon" id="telefon" pattern="\d{3}\ \d{6,7}" required placeholder="123 1234567" value="<?php echo $korisnik['telefon'] ?>"/></td>
                        </tr>                       
                        <tr>
                            <td><label for="mjesto">Grad</label></td>
                            <td><input id="mjesto" name="mjesto" placeholder="Grad" required value="<?php echo $korisnik['mjesto'] ?>" /></td>
                        </tr>
                        <tr>
                            <td colspan="2" class="center"><input type="submit" name="submit" id="posalji" value="Pošalji"/></td>
                        </tr>
                    </table>
                </form>
            <?php
                    else:
                        echo "<table id=sviKorisnici>";
                        echo "<thead>";
                            echo "<tr><th>ID</th><th>Ime</th><th>Prezime</th><th>Korisničko</th><th>Lozinka</th></tr>";
                        echo "</thead>";
                        echo "<tbody>";
                        $korisnici = $database->find_by_sql("SELECT * FROM korisnici");
                        foreach ($korisnici as $korisnik) {
                            echo '<tr>';
                                echo '<td>'.$korisnik['id'].'</td>';
                                echo '<td>'.$korisnik['ime'].'</td>';
                                echo '<td>'.$korisnik['prezime'].'</td>';
                                echo '<td>'.$korisnik['email'].'</td>';
                                echo '<td>'.$korisnik['password'].'</td>';           
                            echo '</tr>';
                        }
                        echo "</tbody>";
                        echo "</table>";
                    endif;
            ?>
            </section>
            <script type="text/javascript"> initIspis(); </script>
            <footer>
            	<p> Datum izrade: travanj 2013. | Vrijeme utrošeno u izradu: 3 sata </p>
                <p> Copyright © 2013 xyz. All Rights Reserved. Sva prava pridržana. </p>
                <p>
                    <a href="http://validator.w3.org/check?uri=http%3A%2F%2Farka.foi.hr%2FWebDiP%2F2012%2Fvjezba_04%2Fkdomic%2F">
                        <img style="border:0;width:88px;height:31px"
                        src="http://www.fourquarters.biz/images/w3cvalidhtml5.jpg"
                        alt="Valid HTML!"/>
                    </a>

                    <a href="http://jigsaw.w3.org/css-validator/check/referer">
                        <img style="border:0;width:88px;height:31px"
                        src="http://jigsaw.w3.org/css-validator/images/vcss-blue"
                        alt="Valid CSS!"/>
                    </a>
                </p>       
            </footer>

        </div>
    </body>
</html>