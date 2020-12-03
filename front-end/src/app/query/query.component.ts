import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { NotificationService } from '../services/notification.service';



interface Query {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-query',
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.scss']
})
export class QueryComponent implements OnInit {
  queries: Query[] = [
    {value:"0", viewValue: "Accounts"},
    {value:"1", viewValue: "Account Wallet with Money"},
    {value:"2", viewValue: "First Customer"},
    {value:"3", viewValue: "DLCs"},
    {value:"4", viewValue: "Valid Credit Cards between 2020 and 2022"},
    {value:"5", viewValue: "VR Games"},
    {value:"6", viewValue: "Largest Products by Size"},
    {value:"7", viewValue: "Good Vendors"},
    {value:"8", viewValue: "Transactions Related to Product #2"},
    {value:"9", viewValue: "Software"},
    {value:"10", viewValue: "Reviews with Comments"},
    {value:"11", viewValue: "Free Games"},
    {value:"12", viewValue: "Products Sold"},
    {value:"13", viewValue: "All Products by Crystal Dynamics"},
    {value:"14", viewValue: "All Unique Products Sold"},
    {value:"15", viewValue: "Average Age of Customers Related to Amount of Transactions"}
  ];

  sqlQuery: String;
  loading: Boolean = true;
  errors: Array<Object>;
  displayedColumns: string[];
  dataSource :any[];

  constructor(private databaseService: DatabaseService, private ns: NotificationService) { }

  ngOnInit(): void {
    // this.loading = true;
    // this.databaseService.getDropdownOptions().subscribe((res:any) => {
    //   console.log(res);
    //   this.queries = res.responses;
    //   this.loading = false;
    // });
  }

  queryOnChange($event) { 
    this.databaseService.getQuery($event.value).subscribe((res:any) => {
      console.log(res);
      this.sqlQuery = res.query.trim();
      this.errors = res.errors;
      if(this.errors.length > 0) {
        this.ns.error(res.errors.join("\n\n"));
      } else {
        this.ns.success("Successfully Queried");
      }
      console.log(res);
      this.dataSource = res.responses
      this.displayedColumns= Object.keys(this.dataSource[0])
    })
  }

}
