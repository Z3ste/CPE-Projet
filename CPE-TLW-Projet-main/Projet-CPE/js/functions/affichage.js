//////////////////////// Functions //////////////////////////
/*  Tout ce qui est affichage de code HTML dynamique
    au sein des pages */


function header_load()
{
    document.querySelector("header").innerHTML = `            <div class="title">
    <h1 class="effetneon">FunBox</h1>
    </div>
    <h2>Ici on vends du fun !</h2>
    <div class="line"></div>
    <div class="row bg-dark-red p-20px">
    <div class="col-4 center">
        <a class="" href="index.html"><span class="underline underline--bacon">Home</span></a>
    </div>
    <div class="col-4 center">
        <a class="" href="articles.html"><span class="underline underline--bacon">Shop</span></a>
    </div>
    <div class="col-4 center">
        <a class="" href="contact.html"><span class="underline underline--bacon">Contact</span></a>
    </div>
    <div class="col-4 center">
        <a class="" href="panier.html"><span class="underline underline--bacon">Panier</span></a>
    </div>
    </div>`;
}
function footer_load()
{
    document.querySelector("footer").innerHTML = `            <div class="row">
    <div class="col-3">
        <div class="center">
            <h2 class="color-dark-grey">FunBox INC</h2>
            <p class="color-dark-grey">24 Tour de la Part-Dieu<br>69000 Lyon</p>
        </div>
    </div>                
    <div class="col-3">
        <div class="center">
            <p class="color-dark-grey">Plus de 90% de nos clients sont satisfait par nos FunBOX !</p>
        </div>
        
    </div>
</div>`;
}

// Affichage de produits
function afficher_tous_articles(prix=null,poids=null) {
    html_article_content = `<div class="row">`
    // filtrage par prix
    if (prix == null)
    {
        var product_list = PRODUCT_LIST;
    }
    else
    {
        prix=prix.value;
        var product_list = [];
        for (i =0; i < PRODUCT_LIST.length; i ++)
        {
        if (PRODUCT_LIST[i].prix == prix)
        {
            product_list.push(PRODUCT_LIST[i]);
        }
        }
    }
    // filtrage par poids
    if (poids != null)
    {
        poids = poids.value;
        var temp_product_list = [];
        for (i =0; i < product_list.length; i ++)
        {
        console.log(product_list[i].poids);
        if (product_list[i].poids == poids)
        {
            temp_product_list.push(product_list[i]);
        }
        }
        product_list = temp_product_list;
    }
    // affichage en grid
    for(var i= 0; i < product_list.length; i++)
    {
        if (i % 3 == 0 && i != 0)
        {
            html_article_content += `</div>`;
            html_article_content += `<div class="row ">`;
        }
        html_article_content += product_list[i].afficher();
    }
    html_article_content += `</div>`
    if (product_list.length == 0)
    {
        html_article_content = "<h3 class='center'>Aucun article :(</h3>"
    }
    document.getElementById("tous-articles").innerHTML = html_article_content;
}

function afficher_un_article(id) {
    var option_color = `<select id="select-color" onChange="generate_image(this.value,'${PRODUCT_LIST[id].calque1}',this)">`; // Calque0 = Choix de la couleur
    for (const [key, value] of Object.entries(COLOR_LIST)) {
    option_color += `<option value="${value}">${key}</option>`;
    }
    option_color += `</select>`;
    html_article_content = `<div class="row">
    <div class="col-2" id="produit-img">
        <img height="500px" width="500px" id="produit-img-img" src="${PRODUCT_LIST[id].img}" alt="Funbox">
        <canvas id="produit-img-canvas"></canvas>
    </div>                
    <div class="col-2">
        <div class="mt-150px">
            <h1>${PRODUCT_LIST[id].nom}</h1>
            <p>${PRODUCT_LIST[id].description}</p>
            <ul>
                <li><img class="icone" src="img/icone/délai.png" />Livraison: 2-3 jours</li>
                <li><img class="icone" src="img/icone/poids.png" />Poids: ${PRODUCT_LIST[id].poids}</li>
                <li><img class="icone" src="img/icone/provenance.png" />Provenance: ${PRODUCT_LIST[id].provenance}</li>
                <li><img class="icone" src="img/icone/prix.png" />Prix: ${PRODUCT_LIST[id].prix}€</li>
            </ul>
            <p>Couleur: ${option_color}</p>
            <p>Quantité: <input id="select-quantity" type="number" name="quantity" value="1"/> </p>
            <input id="article-id" type="hidden" name="id" value="${PRODUCT_LIST[id].id}"/>
            <a href="#" class="link-button mt-150px" onclick="treat_panier();">Ajouter au panier</a>
        </div>
        
    </div>
    </div>`
    document.getElementById("un_article").innerHTML = html_article_content;
}

// Affichage + Gestion du panier
function afficher_mon_panier()
{
    var prix_total = 0;
    var nombre_article = 0;
    var reduction = "Aucune reduction";
    var html_panier_content = `<h3>Vous avez ${PANIER.length} articles dans votre panier</h3>`;
    for (var i= 0; i < PANIER.length; i++)
    {
    prix_total += PRODUCT_LIST[PANIER[i].id].prix*PANIER[i].quantity;
    console.log("id",PANIER[i].id);
    nombre_article += PANIER[i].quantity;
    html_panier_content += `
    <div class="row">
        <div class="col-6">
            <img class="small-image" src="${PRODUCT_LIST[PANIER[i].id].img}" alt="Funbox">
        </div>
        <div class="col-6">
            <p class="center">${PRODUCT_LIST[PANIER[i].id].nom}</br><em>couleur - ${PANIER[i].color}</em></p>
        </div>
        <div class="col-6">
            <p>${PRODUCT_LIST[PANIER[i].id].prix}€</p>
        </div>
        <div class="col-6">
            <p>x${PANIER[i].quantity} <span class="badge-green">En stock</span></p>
            
        </div>
        <div class="col-6">
            <p>${PRODUCT_LIST[PANIER[i].id].prix*PANIER[i].quantity}€</p>
        </div>
        <div class="col-6">
            </br>
            <a class="mini-button" href="?supprimer-${i}">X</a>
        </div>

    </div>`;
    }
    if (nombre_article > 10)
    {
    reduction = "Remise de <span class='badge-green'>10%</span>"
    prix_total *= (90/100)
    }
    html_panier_content += `<div class="row">
    <div class="col-6"></div>
    <div class="col-6"></div>
    <div class="col-6"></div>
    <div class="col-6"></div>
    <div class="col-6">${reduction}<h2>Total: ${prix_total}€</h2></div>
    <div class="col-6"></div>
    <br>
    <a href="?checkout" class="center mt-150px link-button"><img class="icone" src="img/icone/paiement-securise.png" /> Passer au paiement </a>
    `;
    document.getElementById("mon-panier").innerHTML = html_panier_content;

}

// Affichage + Gestion des details du paiement/livraison
function afficher_checkout()
{
    var prix_total = 0;
    var nombre_article = 0;
    var reduction = "Aucune reduction";
    for (var i= 0; i < PANIER.length; i++)
    {
    prix_total += PRODUCT_LIST[PANIER[i].id].prix*PANIER[i].quantity;
    nombre_article += PANIER[i].quantity;
    }
    if (nombre_article > 10)
    {
    reduction = "Remise de <span class='badge-green'>10%</span>"
    prix_total *= (90/100)
    }
    var today = new Date().toISOString().slice(0, 10);
    html_checkout_content = `
    <form>
    <div class="row">
        <div class="col-2">
            <p><u>Vos informations</u></p>
            <input style="width: 45%" id="input-nom" type="text" placeholder="NOM" required/>
            <input style="width: 45%" id="input-prenom" type="text" placeholder="Prenom" required/>
            <input id="input-tel" type="tel" placeholder="N° de téléphone" required/>
            <input id="input-email" type="email" placeholder="adresse email" required/>
            <br><br>
            <p><u>Votre moyen de paiement</u></p>
            <input id="input-carte" type="text" placeholder="N° de la carte"/>
            <input style="width: 45%" id="input-carte-expi" type="text" placeholder="Date d'expiration"/>
            <input style="width: 45%" id="input-carte-cvv" type="text" placeholder="CVV"/>
            <br><br>
            <p><u>Information optionnelle</u></p>
            <textarea id="input-specialdemande" placeholder=" Une consigne à apporter à la commande"></textarea>
        </div>
        <div class="col-2">
            <p><u>Detail sur la livraison</u></p>
            <input id="input-adresse1" type="text" placeholder="Adresse" required/>
            <input style="width: 45%" id="input-adresse2" type="text" placeholder="Code postal" required/>
            <input style="width: 45%" id="input-adresse3" type="text" placeholder="Ville" required/>
            <br>Date de livraison: <input style="width: 45%" id="input-date" type="date" placeholder="Date de livraison" value="${today}" required/>
            <a class="center mt-150px link-button" onclick="geoloc(${prix_total})">Calculer</a>
            <br><br><input type="checkbox" id="input-express" onchange="livraison_express(${prix_total})"><label for="input-express">Livraison express (+8€)</label>
            <p style="font-size: 10px"><em>* Toutes nos livraison sont expédié depuis Lyon</em></p>
            <div class="row">
            <div class="col-2">
                <img class="bordure-img" src="https://api.mapbox.com/v4/mapbox.satellite/${ZOOM}/${lon2tile(POS_SIEGE_x,ZOOM)}/${lat2tile(POS_SIEGE_y,ZOOM)}.jpg90?access_token=${TOKEN}" alt="adresse-depart"/>
            </div>
            <div class="col-2">
                <img class="bordure-img" style="height: 256px;" id="adresse-map" src="img/unknown.png" alt="adresse-arrivé"/>
            </div>
            </div>
            <br><br>
            <p><u>Prix total</u></p>
            <ul>
            <li>${nombre_article} articles</li>
            <li>${reduction}</li>
            <li id="express-livraison">Frais de livraison express <span class='badge-red'>8€</span></li>
            <li id="long-livraison">Frais de livraison longue distance<span class='badge-red' id="long-livraison-frais">8€</span></li>
            <h2>Total: <span id="prix-tot">${prix_total}</span>€
            </ul>
            </div>

    </div>
    <div class="row">
        <input class="center mt-150px link-button" type="reset"/>
        <a href="?complete" class="center mt-150px link-button"><img class="icone" src="img/icone/paiement-securise.png" /> Payer </a>
    </div>
    </form>
    `;
    document.getElementById("mon-panier").hidden = true;
    document.getElementById("checkout").innerHTML = html_checkout_content;
    document.getElementById("express-livraison").hidden = true;
    document.getElementById("long-livraison").hidden = true;
}

function livraison_express(prix_total)
{
  if (document.getElementById("input-express").checked == true)
  {
    document.getElementById("express-livraison").hidden = false;
    if (parseFloat(document.getElementById("prix-tot").innerHTML) != prix_total)
    {
      document.getElementById("prix-tot").innerHTML = parseFloat(document.getElementById("prix-tot").innerHTML) + 8;
    }
    else
    {
      document.getElementById("prix-tot").innerHTML = prix_total + 8;
    }
    
  }
  else
  {
    document.getElementById("express-livraison").hidden = true;
    if (parseFloat(document.getElementById("prix-tot").innerHTML) != prix_total)
    {
      document.getElementById("prix-tot").innerHTML = parseFloat(document.getElementById("prix-tot").innerHTML) - 8;
    }
    else
    {
      document.getElementById("prix-tot").innerHTML = prix_total;
    }

  }
}

function geoloc(prix_total)
{
  var zoom = ZOOM;
  var erreur = "ok"
  var rue= document.getElementById("input-adresse1").value.toLowerCase();
  var ville = document.getElementById("input-adresse3").value;
  var code_postal = document.getElementById("input-adresse2").value;
  var adresse = rue + " " + ville + " France";
  var apiURL = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + encodeURI(adresse) + ".json?access_token=" + TOKEN;
  console.log(apiURL);
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", apiURL, false ); 
  xmlHttp.send( null );
  adresse_content = JSON.parse(xmlHttp.responseText);
  if ((adresse_content["features"].length > 0))
  {
    var x,y;
    x = adresse_content["features"][0]["geometry"]["coordinates"][0];
    y = adresse_content["features"][0]["geometry"]["coordinates"][1];
    console.log("x=",x," y=",y);
    img = `https://api.mapbox.com/v4/mapbox.satellite/${zoom}/${lon2tile(x,zoom)}/${lat2tile(y,zoom)}.jpg90?access_token=${TOKEN}`;
    document.getElementById("adresse-map").src = img;
    console.log(img);
    
    apiURL2 = `https://api.mapbox.com/directions/v5/mapbox/driving/${POS_SIEGE};${x},${y}?access_token=${TOKEN}`;
    console.log(apiURL2);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", apiURL2, false ); 
    xmlHttp.send( null );
    trajet_info = JSON.parse(xmlHttp.responseText);
    console.log(trajet_info);
    trajet_temps = trajet_info["routes"][0]["duration"] /3600;
    trajet_distance = trajet_info["routes"][0]["distance"] /1000;
    console.log("Durée du trajet: ",trajet_temps, " heures");
    console.log("Distance du trajet: ",trajet_distance, " km");
    if (trajet_distance > 20.0)
    {
      console.log("Trajet > 20km");
      document.getElementById("long-livraison").hidden = false;
      document.getElementById("long-livraison-frais").innerText = Math.round((5 + 0.07*trajet_distance)* 100) / 100;
      if (document.getElementById("input-express").checked == true)
      {
        document.getElementById("prix-tot").innerHTML = prix_total + 8 + Math.round((5 + 0.07*trajet_distance)* 100) / 100;
      }
      else
      {
        document.getElementById("prix-tot").innerHTML = prix_total + Math.round((5 + 0.07*trajet_distance)* 100) / 100;
      }
      
    }
    else if (document.getElementById("long-livraison").hidden == false)
    {
      document.getElementById("long-livraison").hidden = true;
      if (document.getElementById("input-express").checked == true)
      {
        document.getElementById("prix-tot").innerHTML = prix_total + 8;
      }
      else
      {
        document.getElementById("prix-tot").innerHTML = prix_total;
      }   
    }
  }
  else
  {
    erreur = "adresse invalide"
    console.log(erreur)
  }
}