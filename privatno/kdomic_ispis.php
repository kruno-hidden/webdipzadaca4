<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" type="text/css" href="../css/kdomic_main.css" />
        <link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.css" />        
        <script type="text/javascript" src="../js/jquery.min.js"></script>
        <script type="text/javascript" src="../js/jquery.dataTables.js"></script>        
    </head>

    <body>
        <div id="outerDiv">
            <header>
                <nav id="mainMenu">
                    <ul>
                        <li><a href="kdomic_index.html" class="current">Početna</a></li>                        
                        <li><a href="kdomic_register.php">Registracija</a></li>
                        <li><a href="kdomic_login.html">Prijava</a></li>
                        <li><a href="kdomic_tablica.php" >Tablica</a></li>
                        <li><a href="kdomic_dijagrami.html">Dijagrami</a></li>
                    </ul>
                </nav>
                <h1>Krunoslav Domić </h1>
            </header>

            <div class="subMenu"> </div>

            <section>
            <?php
                    require("korisnici.php");
                    echo "<table id=sviKorisnici>";
                    echo "<thead>";
                        echo "<tr><th>ID</th><th>Ime</th><th>Prezime</th><th>Korisničko</th><th>Lozinka</th></tr>";
                    echo "</thead>";
                    echo "<tbody>";
                    $database = new KorisnikBAZA(); 
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
            ?>
            </section>
            <script type="text/javascript">$('#sviKorisnici').dataTable();</script>
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