import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs';

import { Hero } from './hero';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class HeroService {

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  }

  constructor(
    private messageService: MessageService,
    private http: HttpClient
  ) { }

  private log(message: string) {
    this.messageService.add(`HeroService: ${message}`);
  }

  private heroUrl = 'http://127.0.0.1:8000/hero/';  // URL to web api

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      this.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }

  getHeroes(): Observable<Hero[]> {
    return this.http.get<Hero[]>(
      this.heroUrl+'list', { responseType: 'json'}
    ).pipe(
      tap(heroes => this.log(`fetched ${heroes.length} heroes`)),
      catchError(this.handleError('getHeroes', []))
    );
  }
  getHero(id: number): Observable<Hero> {
    return this.http.get<Hero>(
      `${this.heroUrl}${id}`, { responseType: 'json'}
    ).pipe(
      tap(_ => this.log(`fetched hero id=${id}`)),
      catchError(this.handleError<Hero>(`getHero id=${id}`))
    );
  }

  updateHero(hero: Hero): Observable<any> {
    return this.http.patch(
      this.heroUrl+hero.id, hero, this.httpOptions
    ).pipe(
      tap(_ => this.log(`updated hero id=${hero.id}`)),
      catchError(this.handleError<any>('updateHero'))
    );
  }

  addHero(hero: Hero): Observable<Hero> {
    return this.http.post<Hero>(
      this.heroUrl+'create', hero, this.httpOptions
    ).pipe(
      tap((newHero: Hero) => this.log(`added hero w/ id=${newHero.id}`)),
      catchError(this.handleError<Hero>('addHero'))
    );
  }

  deleteHero(id: number): Observable<Hero> {
    return this.http.delete<Hero>(
      `${this.heroUrl}${id}`, this.httpOptions
    ).pipe(
      tap(_ => this.log(`delete hero id=${id}`)),
      catchError(this.handleError<Hero>('deleteHero'))
    )
  }

  searchHeroes(term: string): Observable<Hero[]> {
    if (!term.trim()) {
      // if not search term, return empty hero array.
      return of([])
    }
    return this.http.get<Hero[]>(
      `${this.heroUrl}search/?name=${term}`
    ).pipe(
      tap(
        heroes => heroes.length ?
        this.log(`found ${heroes.length} heroes match "${term}"`) :
        this.log(`no hero match ${term}`)
      ),
      catchError(this.handleError<Hero[]>('searchHeroes', []))
    )
  }
}
