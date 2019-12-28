import {ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ProductInfo} from "../_models";
import {Observable} from "rxjs";
import {ListLaunchService} from "../_services";

@Component({
    selector: 'app-list-launches',
    templateUrl: './list-launches.component.html',
    styleUrls: ['./list-launches.component.scss'],
    encapsulation: ViewEncapsulation.None,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class ListLaunchesComponent implements OnInit {

    list_launches$: Observable<ProductInfo[]>;
    now: number;
    show_spinner: boolean = true;

    constructor(private listLaunchService: ListLaunchService,
                private changeDetectorRef: ChangeDetectorRef) {
    }

    ngOnInit() {

        // Load the data every 5 seconds
        setInterval(() => {
            this.loadAll();
            this.now = Date.now();
            this.changeDetectorRef.markForCheck();
            this.show_spinner = false;
        }, 5000);

    }

    loadAll() {
        this.list_launches$ = this.listLaunchService.list_launches;
        this.listLaunchService.loadAll();
    }

}


