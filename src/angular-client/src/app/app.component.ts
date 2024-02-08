import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [RouterOutlet],
  template: ``,
  styleUrl: "./app.component.sass",
})
export class AppComponent {
  title = "angular-client";
}
