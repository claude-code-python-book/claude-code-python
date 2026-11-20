BEGIN;
SELECT balance FROM loyalty_accounts WHERE customer_id = 1 FOR UPDATE \gset
SELECT pg_sleep(0.5) \g /dev/null
SELECT :balance >= 600 AS ok \gset
\if :ok
  UPDATE loyalty_accounts SET balance = :balance - 600 WHERE customer_id = 1;
  INSERT INTO points_entries (customer_id, kind, points) VALUES (1, 'redeem', -600);
  \echo request: read balance :balance, redeemed 600
\else
  \echo request: read balance :balance, refused
\endif
COMMIT;
