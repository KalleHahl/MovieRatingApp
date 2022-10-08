# Elokuvasovellus
Sovelluksen avulla voi kirjata ylös katsomiaan elokuvia ja antaa niille arvostelun.

### Linkki sovellukseen:

* Suosittelen lisäämään elokuvat Pulp Fiction (ohjaaja: Quentin Tarantino, julkaisu: 1994) ja Memoria (ohjaaja: Apitchatpong Weerasethakul, julkaisu: 2021), näille elokuville on muiden käyttäjien jättämiä arvosteluja
* [Elokuvakirjasto](https://tsoha-elokuvakirjasto.herokuapp.com/) 

### Tämän hetkinen tilanne:

* Sovellukseen voi rekisteröidä käyttäjän ja kirjautua sisään
* Kirjautumisen jälkeen aukeaa käyttäjän etusivu, jossa on mahdollisuudet lisätä elokuva tai ohjaaja tai kirjautua ulos
* Elokuvan ja ohjaajan lisäys toimii ainakin omilla testeillä moitteettomasti
* Jos käyttäjä on lisännyt elokuvia tai ohjaajia, tulevat ne näkyviin etusivulle
* Etusivulta voi klikata omia elokuvia, joka vie elokuvan omalle sivulle, jossa voi itse antaa arvostelun ja jossa näkee myös muiden käyttäjien arvosteluja kyseiselle elokuvalle
* Error sivutkin ovat kohdillaan, elokuvien/ohjaajien nimet eivät voi olla liian pitkiä (100 chr) eikä syntymä/julkaisuvuoteen voi laittaa kuin lukuja. Pituus pätee myös käyttäjänimelle ja salasanalle ja rekisteröidessä salasanojen on oltava samat.

### Sovelluksen ominaisuudet:

* Käyttäjä voi kirjautua omilla luoduilla tunnuksilla sisään
* Käyttäjä voi kirjata ylös katsomansa elokuvan
* Elokuville voi jättää arvosanan 1-10 ja kirjoittaa lyhyen teksti arvostelun
* Käyttäjät voivat tutkia toisten käyttäjien antamia elokuva-arvosteluja
