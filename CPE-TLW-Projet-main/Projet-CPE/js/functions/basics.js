//////////////////////// Functions //////////////////////////

function lon2tile(lon,zoom=10) { return (Math.floor((lon+180)/360*Math.pow(2,zoom))); }
function lat2tile(lat,zoom=10)  { return (Math.floor((1-Math.log(Math.tan(lat*Math.PI/180) + 1/Math.cos(lat*Math.PI/180))/Math.PI)/2 *Math.pow(2,zoom))); }



function generate_image(calque0,calque1,self)
{
  console.log(self.options[self.selectedIndex].text);
  document.getElementById("select-color").style.setProperty("background-color",self.options[self.selectedIndex].text);
  document.getElementById("produit-img").innerHTML = `<canvas height="800px" width="800px" id="produit-img-canvas" ></canvas>`;
  var canvas_e = document.querySelector('#produit-img-canvas');
  var ctx = canvas_e.getContext("2d");
  console.log("Changing the image");
  // Calque 1
  var img_calque1 = new Image(); 
  img_calque1.src = calque1;
  img_calque1.onload = function() {
    ctx.drawImage(img_calque1,0,0);
    // Calque 1
    var img_calque0 = new Image(); 
    img_calque0.src = calque0; 
    img_calque0.onload = function() {
      ctx.drawImage(img_calque0,0,0);
    };
  };  
 
}

function getCook(cookiename) 
  {
  var cookiestring=RegExp(cookiename+"=[^;]+").exec(document.cookie);
  return atob(decodeURIComponent(!!cookiestring ? cookiestring.toString().replace(/^[^=]+./,"") : "").replace("@", "="));
  }
function setCook(cname, cvalue) 
{
    if ('btoa' in window) {
        cvalue = btoa(cvalue).replace("=", "@");
    }
    document.cookie = cname + "=" + cvalue + ";";
}
function first_generate_cookie()
{
  var panier = [];
  setCook("panier",JSON.stringify(panier))
  return panier;
}
function first_treat_cookie()
{
  var panier = JSON.parse(getCook("panier"));
  return panier;
}

function treat_panier()
{
  var color = document.getElementById('select-color').options[document.getElementById('select-color').selectedIndex].text;
  var quantity = document.getElementById('select-quantity').value;
  var article_id = document.getElementById('article-id').value;
  add_item_panier(article_id,color,quantity);
}

function save_cookie()
{
  setCook("panier",JSON.stringify(PANIER))
}

function add_item_panier(item_id,item_color = "red",item_quantity = 1)
{
  article = {"id":item_id,"color":item_color,"quantity":item_quantity};
  PANIER.push(article);
  save_cookie();
}
function delete_item_panier(id)
{
  PANIER.splice(id, 1);
  save_cookie();
}

// Recuperation des produits/des personnalisations
function parseProduits(content) {
    console.log("Length: ",content["article-list"].length);
    for(var i= 0; i < content["article-list"].length; i++)
    {
         console.log(content["article-list"][i]); // Log purpose
         PRODUCT_LIST[i] = new produit(content["article-list"][i]);
    } 
  }
  function parseCouleur(content) {
    console.log("Length: ",content["couleur-list"].length);
    COLOR_LIST = content["couleur-list"];
  }
  
  