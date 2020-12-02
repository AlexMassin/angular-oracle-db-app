import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  url: String = "/api/v1/";

  constructor(private http: HttpClient) { }
  

  createDB() {
    return this.http.get(this.url + "crud/create");
  }

  destroyDB() {
    return this.http.get(this.url + "crud/destroy");
  }

  testDB() {
    return this.http.get(this.url + "crud/ping");
  }

  populateDB() {
    return this.http.get(this.url + "crud/populate");
  }

  getQuery(id) {
    return this.http.get(this.url + `crud/sample-query/${id}`);
  }

  getDropdownOptions() {
    return this.http.get(this.url + "stats/samples");
  }

  getRawQuery(queryString) {
    return this.http.get(this.url + `/crud/raw-query/${queryString}`);
  }
}
