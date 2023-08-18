//////////////////////// Objects //////////////////////////
/*              Objet produit                   */
/* Caracterise les differents produits du site  */
function produit(jsonobject) {
    this.id = jsonobject.id;
    this.nom = jsonobject.nom;
    this.description = jsonobject.description;
    this.prix = jsonobject.prix;
    this.poids = jsonobject.poids;
    this.quantité = jsonobject.quantité;
    this.provenance = jsonobject.provenance;
    this.img = jsonobject.img;
    this.calque1 = jsonobject.calque1;
    this.afficher = function() {
      return `<div class=col-3>
      <a href="perso.html?article-${this.id}">
          <img src="${this.img}" class="medium-image mr-20px" />
      </a>
      <br><span style="font-size: 30px">${this.nom}</span>
      </br>
      <p>
          ${this.prix}€
      </p>
  
  </div>`;
    }
  
  }