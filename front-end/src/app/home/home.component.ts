import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { NotificationService } from '../services/notification.service';

import TypeIt from "typeit";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  sqlQuery: String;
  loading: Boolean = false;
  errors: Array<Object>;

  constructor(private databaseService: DatabaseService, private ns: NotificationService) { }

  ngOnInit(): void {
    new TypeIt("#description", {speed: 50})
    .type("A Place for You to")
    .pause(1000)
    .type(" Create, ")
    .pause(1000)
    .type("Delete, ")
    .pause(1000)
    .type("and Modify the Tables.")
    .pause(1000)
    .go();

  }

  createDBAction() {
    this.loading = true;
    this.databaseService.createDB().subscribe((res:any) => {
      this.sqlQuery = res.query.trim();
      this.errors = res.errors;
      if(this.errors.length > 0) {
        this.ns.error(res.errors.join("\n\n"));

      } else {
        this.ns.success("Successfully Created Tables");
      }
      console.log(res);
      this.loading = false;
    })
  }

  destroyDBAction() {
    this.loading = true;
    this.databaseService.destroyDB().subscribe((res:any) => {
      this.sqlQuery = res.query.trim();
      this.errors = res.errors;
      if(this.errors.length > 0) {
        this.ns.error(res.errors.join("\n\n"));
      } else {
        this.ns.success("Successfully Dropped Tables");
      }
      console.log(res);
      this.loading = false;
    })
  }

  populateDBAction() {
    this.loading = true;
    this.databaseService.populateDB().subscribe((res:any) => {
      this.sqlQuery = res.query.trim();
      this.errors = res.errors;
      if(this.errors.length > 0) {
        this.ns.error(res.errors.join("\n\n"));
      } else {
        this.ns.success("Successfully Populated Tables");
      }
      console.log(res);
      this.loading = false;
    })
  }

  testDBAction() {
    this.loading = true;
    this.databaseService.testDB().subscribe((res:any) => {
      this.sqlQuery = res.query.trim();
      this.errors = res.errors;
      if(this.errors.length > 0) {
        this.ns.error(res.errors.join("\n\n"));
      } else {
        this.ns.success("Successfully Connected");
      }
      console.log(res);
      this.loading = false;
    })
  }

}
