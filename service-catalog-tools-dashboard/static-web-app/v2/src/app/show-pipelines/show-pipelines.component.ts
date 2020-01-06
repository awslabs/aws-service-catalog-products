import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {PipelineInfo} from "../_models";
import {PipelineStatusService} from "../_services/pipeline-status.service";

@Component({
    selector: 'app-show-pipelines',
    templateUrl: './show-pipelines.component.html',
    styleUrls: ['./show-pipelines.component.scss']
})
export class ShowPipelinesComponent implements OnInit {

    pipelines$: Observable<PipelineInfo[]>;
    now: number;
    show_spinner: boolean = true;

    constructor(private pipelineStatusService: PipelineStatusService,
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
        this.pipelines$ = this.pipelineStatusService.pipelines;
        this.pipelineStatusService.loadAll();
    }

}
