import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar'

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  
  constructor(public snackBar: MatSnackBar ) {}

  config: MatSnackBarConfig = {
    duration: 20000,
    horizontalPosition: 'right',
    verticalPosition: 'top'
  }

  success(msg:string) {
    this.config['panelClass'] = ['success', 'notification']
    this.snackBar.open(msg,'Close', this.config)
  }

  error(msg:string) {
    this.config['panelClass'] = ['error', 'notification']
    this.snackBar.open(msg,'Close', this.config)
  }
}