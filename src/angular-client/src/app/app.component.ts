import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  template: ` Welcome to Angular! {{ title }} `,
  standalone: true,
})
export class AppComponent {
  title = "test4";
}
