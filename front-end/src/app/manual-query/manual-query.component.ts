import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { NotificationService } from '../services/notification.service';

interface Query {
  value: string;
  viewValue: string;
}


@Component({
  selector: 'app-manual-query',
  templateUrl: './manual-query.component.html',
  styleUrls: ['./manual-query.component.scss']
})
export class ManualQueryComponent implements OnInit {

  queries: Query[] = [];

  sqlQuery: String;
  loading: Boolean = true;
  errors: Array<Object>;
  displayedColumns: string[];
  dataSource :any[];
  showTable: Boolean = false;

  constructor(private databaseService: DatabaseService, private ns: NotificationService) { }

  ngOnInit(): void {}

  queryOnSubmit() { 
   this.databaseService.getRawQuery(this.sqlQuery).subscribe((res:any) => {
    this.errors = res.errors;
    if(this.errors.length > 0) {
      this.ns.error(res.errors.join("\n\n"));
    } else {
      this.ns.success("Successfully Queried");
    }
    console.log(res);
    this.dataSource = res.responses
    if (typeof(this.dataSource) !== 'string') {
      this.showTable = true
      this.displayedColumns=Object.keys(this.dataSource[0])
    } else {
      this.showTable = false
    }
   });
  }

  saveQuery($event) {
    this.sqlQuery = $event.target.value;
  }
}
