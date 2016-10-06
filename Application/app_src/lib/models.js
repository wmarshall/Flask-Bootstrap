import $ from "jquery";

class ViewModel {

  constructor(attrs){
    for(var attr in attrs){
      this[attr] = attrs[attr];
    }
  }

  static get endpoint(){
    return "/rest/";
  }

  get cls(){
    return ViewModel;
  }

  get pkey(){
    return [];
  }

  get pkey_obj(){
    let obj = {};
    const pkey = this.pkey;
    for (var i = 0; i < pkey.length; i++) {
      const key = pkey[i];
      obj[key] = this[key];
    }
    return obj;
  }

  get cols(){
    return [];
  }

  get cols_obj(){
    let obj = {};
    const cols = this.cols;
    for (var i = 0; i < cols.length; i++) {
      const col = cols[i];
      obj[col] = this[col];
    }
    return obj;
  }

  static filter2path(filter){
    let filterpath = "";
    for (var key in filter) {
      if(filter[key] != null && filter[key] != ""){
        filterpath += `${key}/${filter[key]}/`;
      }
    }
    if(filterpath.endsWith("/")){
      filterpath = filterpath.substring(0, filterpath.length - 1);
    }
    return filterpath;
  }

  static get(filter = {}){
    const raw_promise = $.ajax(this.endpoint + this.filter2path(filter), {
      method: "GET",
    });
    const resource_promise = new Promise((resolve, reject) => {
      raw_promise.done((data) => {
        const resources = [];
        for(var resource_idx in data.resources){
          resources.push(new this(data.resources[resource_idx]));
        }
        return resolve(resources);
      }).fail(() => {
        return reject("AJAX Fail");
      });
    });
    return resource_promise;
  }


  create(){
    return $.ajax(this.cls.endpoint, {
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(this.cols_obj),
    });
  }

  update(){
    return $.ajax(this.cls.endpoint, {
      method: "PUT",
      contentType: "application/json",
      data: JSON.stringify(this.pkey_obj),
    });
  }

  delete(){
    return $.ajax(this.cls.endpoint, {
      method: "DELETE",
      contentType: "application/json",
      data: JSON.stringify(this.pkey_obj),
    });
  }

}
