-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


--create database tournament

-- allow for multiple tournaments
create table tournament (
    id serial primary key,
    name text not null,
    start_date date not null,
    end_date date not null,
    unique (name, start_date, end_date));
comment on table tournament is 'This contains all the tournaments players participate in. One player can be in multiple tournaments.  Tournaments can have the same name but not the same name, start and end.'; 
comment on column tournament.id is 'This is the relational primary key of the table and is unique among all records in the table.';
comment on column tournament.name is 'This is the name of the tournament.';
comment on column tournament.start_date is 'This is the date the tournament starts.';
comment on column tournament.end_date is 'This is the date the tournament finishes.';


-- allow for remembering players for a given tournament
create table player (
    id serial primary key,
    name text not null,
    tournament_id integer references tournament(id) null,
    unique (id, tournament_id));
comment on table player is 'Each row in this table contains information about an individual player.'; 
comment on column player.id is 'This is the relational primary key of the table and is unique among all records in the table.';
comment on column player.name is 'This is the name of the player.';
comment on column player.tournament_id is 'This is a relational foreign key to the tournament the player is in. If this is null or blank, it means that the player has registered but is not playing in a tournament.';


--allow the ability to keep track of matches between players
create table match (
    id serial primary key,
    winner_id integer references player(id) not null,
    loser_id integer references player(id) not null,
    tournament_id integer references tournament(id) not null,
    unique (winner_id, loser_id, tournament_id));
comment on table match is 'Each row in this table contains information about the results of a match between two players.'; 
comment on column match.id is 'This is the relational primary key of the table and is unique among all records in the table.';
comment on column match.winner_id is 'This is a relational foreign key to the player that won the match.';
comment on column match.loser_id is 'This is a relational foreign key to the player that lost the match.';
comment on column match.tournament_id is 'This is a relational foreign key to the tournament the match was played in.';


--simplified database view to provide count of wins by player
create view player_win_count as
select
    c.name as tournament_name,
    a.winner_id,
    count(*) as win_count
from match a
    join player b on b.id = a.winner_id
    join tournament c on c.id = b.tournament_id and c.id = a.tournament_id
group by
    c.name,
    a.winner_id;
comment on view player_win_count is 'This database view provides a summarized count of wins by player by tournament.';
comment on column player_win_count.tournament_name is 'The name of the tournament for the winning player winner_id.';
comment on column player_win_count.winner_id is 'The identifier of the winning player winner_id.';
comment on column player_win_count.win_count is 'The number of wins for the winning player winner_id';


--simplified database view to provide count of losses by player
create view player_loss_count as
select
    c.name as tournament_name,
    a.loser_id,
    count(*) loss_count
from match a
    join player b on b.id = a.winner_id
    join tournament c on c.id = b.tournament_id and c.id = a.tournament_id
group by
    c.name,
    a.loser_id;
comment on view player_loss_count is 'This database view provides a summarized count of losses by player by tournament.';
comment on column player_loss_count.tournament_name is 'The name of the tournament for the losing player loser_id.';
comment on column player_loss_count.loser_id is 'The identifier of losing player loser_id.';
comment on column player_loss_count.loss_count is 'The number of losses for losing player loser_id.';


--simplified database view to provide match counts by player
create view player_match_count as
select
    c.name as tournament_name,
    p.id as player_id,
    (coalesce(w.win_count,0) + coalesce(l.loss_count,0)) as match_count
from player p
    join tournament c on c.id = p.tournament_id
    left join player_win_count w on w.winner_id = p.id
    left join player_loss_count l on l.loser_id = p.id
group by c.name, p.id, (coalesce(w.win_count,0) + coalesce(l.loss_count,0));
comment on view player_match_count is 'This database view provides a summarized count of matches by player by tournament.';
comment on column player_match_count.tournament_name is 'The name of the tournament for the player player_id.';
comment on column player_match_count.player_id is 'This is the a relational reference to the player in the match.';
comment on column player_match_count.match_count is 'The number of matches played by the player player_id.';
