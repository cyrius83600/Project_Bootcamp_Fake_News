import { Component } from '@angular/core';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'fake-component',
  standalone: true,
  imports: [HeaderComponent],
  templateUrl: './fake.component.html',
  styleUrl: './fake.component.css'
})
export class FakeComponent {

}
