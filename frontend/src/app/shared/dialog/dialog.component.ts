import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export type DialogType = 'confirmation' | 'error' | 'message';

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

  ok() {
    this.closed.emit(true);
  }

  cancel() {
    this.closed.emit(false);
  }
}
