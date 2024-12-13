import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FakeComponent } from './fake/fake.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FakeComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'FakeNews';
}
