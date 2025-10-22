import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export type DialogType = 'confirmation' | 'error' | 'message' | 'rating';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css'],
  imports:[CommonModule, FormsModule],
  standalone: true
})
export class DialogComponent {
  @Input() type: DialogType = 'message';
  @Input() title: string = 'Dialog';
  @Input() message: string = '';

  @Output() closed = new EventEmitter<boolean>();
  @Output() rated = new EventEmitter<number>();

  rating: number = 5;


  ok() {
    if (this.type === 'rating') {
      this.rated.emit(this.rating);
      return;
    }
    this.closed.emit(true);
  }

  cancel() {
    this.closed.emit(false);
  }
}
