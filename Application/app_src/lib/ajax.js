import "babel-polyfill";
import _AjaxInterceptor from "ajax-interceptor";
import $ from "jquery";
import {makeMessage, makeMessagesCloseable} from "./messages";



function overrideFormSubmit(){
  /*
  All form submits are ajax for error display.
  */
  $("form").submit( event => {
    if(event.target.getAttribute("action") != null){
      event.preventDefault();
      const url = event.target.action;
      const method = event.target.method;
      const data = {};
      for (let i = event.target.length - 1; i >= 0; i--) {
        let name = event.target[i].name;
        let content = $(event.target[i]).val();
        data[name] = content;
      }
      return $.ajax(url, {
        "method": method,
        "data": data
      });
    }
  });
}


$(
  _AjaxInterceptor.addResponseCallback(function(xhr) {
    if(xhr.getResponseHeader("Content-Type") === "application/json"){
      const resp_obj = JSON.parse(xhr.response);
      const messages = resp_obj["messages"];
      if(messages){
        for (let i = 0; i < messages.length; i++) {
          const [category, messagetext] = messages[i];
          makeMessage(messagetext, category);
        }
      }
      const redirect = resp_obj["redirect"];
      if(redirect){
        //TODO: Deal with location.hash
        location.assign(redirect);
      }

    }
  })
);
$(function(){
  overrideFormSubmit();
  makeMessagesCloseable();
  _AjaxInterceptor.wire();
});

export var AjaxInterceptor = _AjaxInterceptor;

