//////////////////////// Code `onload` //////////////////////////
/*
    Code à lancer au chargement de la page
*/
fetch(url)
.then(res => res.json())
.then(function(response) {
  console.log(' BDD', response); // Log purpose
  parseProduits(response);
  parseCouleur(response);

  if (WHERE == "/articles.html")
  {
    afficher_tous_articles();
  }
  else if (WHERE == "/perso.html")
  {
    if (ARG.includes("article-") && ARG.indexOf("article-") == 1)
    {
      id = ARG.split("article-")[1];
      if (!isNaN(id))
      {
        id = parseInt(id,10);
        afficher_un_article(id);
      }
    }
  }
  else if (WHERE == "/index.html")
  {
    
  }
  else if (WHERE == "/panier.html")
  {

    if (ARG.includes("supprimer-") && ARG.indexOf("supprimer-") == 1)
    {
      id = ARG.split("supprimer-")[1];
      if (!isNaN(id))
      {
        id = parseInt(id,10);
        delete_item_panier(id);
        document.location.href = "/panier.html";
      }
    }
    else if (ARG.includes("checkout") && ARG.indexOf("checkout") == 1)
    {
      afficher_checkout();
    }
    afficher_mon_panier();
  }
  return true;
  
})
.catch(err => { throw err });

// Gestion du panier
if (getCook("panier") == "")
{
  PANIER = first_generate_cookie();
}
else
{
  PANIER = first_treat_cookie();
}
console.log("Panier",PANIER);