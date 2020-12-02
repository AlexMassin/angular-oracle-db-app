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
  queries: Query[] = [];

  sqlQuery: String;
  loading: Boolean = true;
  errors: Array<Object>;
  displayedColumns: string[];
  dataSource :any[];

  constructor(private databaseService: DatabaseService, private ns: NotificationService) { }

  ngOnInit(): void {
    this.loading = true;
    this.databaseService.getDropdownOptions().subscribe((res:any) => {
      console.log(res);
      this.queries = res.responses;
      this.loading = false;
    });
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
