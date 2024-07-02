CREATE DATABASE public WITH ENCODING 'UTF8';



CREATE TABLE tree (
	id			  BIGINT,
	total         BIGINT,
	title 	      TEXT PRIMARY KEY,
    tree      	  TEXT,
    parent        TEXT REFERENCES tree(title)
);

-- Created the elements for each person
INSERT INTO tree(id, total, title, tree, parent) VALUES
	(10, 13, 'Moshe', '1-3-10', 'Yael'),
	(2, 6, 'Haim', '1-1-2', 'Shai'),
	(1, 90, 'Tomer', '1', Null),
	(3, 204, 'Yael', '1-3', 'Tomer'),
	(1, 69, 'Shai', '1-1', 'Tomer'),
	(8, 538, 'Oren', '1-3-8', 'Yael')

	
-- recursive relationship
with recursive cte as
( 
	-- static element for initial entry
	select title, title as tree_descendant, total
	from tree
	union all
	-- union with recursive element
	-- recursively join all descendants to parent to see all the descendants for each parent (including oneself)
	select cte.title, tree.title as tree_descendant, tree.total
	from cte
	join tree on cte.tree_descendant = tree.parent)
	select tree.id, tree.total, cte.title, tree.tree, sum(cte.total) as new_total from cte
	-- rejoin original tree table onto new cte table to see other columns such as id.
	join tree on tree.title = cte.title
    group by cte.title, tree.id, tree.tree, tree.total




